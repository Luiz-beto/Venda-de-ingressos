# app.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'futebol123'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Jogos pré-cadastrados com escudos ATUALIZADOS
jogos = {
    1: {
        'casa': 'Flamengo',
        'fora': 'Palmeiras',
        'escudo_casa': 'https://upload.wikimedia.org/wikipedia/commons/9/93/Flamengo-RJ_%28BRA%29.png',
        'escudo_fora': 'https://upload.wikimedia.org/wikipedia/commons/1/10/Palmeiras_logo.svg',
        'ingressos': 0,
        'preco': 50.00,
        'prevenda': False
    },
    2: {
        'casa': 'Corinthians',
        'fora': 'São Paulo',
        'escudo_casa': 'https://upload.wikimedia.org/wikipedia/pt/archive/b/b4/20250923030059%21Corinthians_simbolo.png',
        'escudo_fora': 'https://upload.wikimedia.org/wikipedia/commons/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg',
        'ingressos': 0,
        'preco': 45.00,
        'prevenda': False
    },
    3: {
        'casa': 'Grêmio',
        'fora': 'Internacional',
        'escudo_casa': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Gremio_logo.svg/250px-Gremio_logo.svg.png',
        'escudo_fora': 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Escudo_do_Sport_Club_Internacional.svg',
        'ingressos': 0,
        'preco': 40.00,
        'prevenda': False
    },
    4: {
        'casa': 'Santos',
        'fora': 'Vasco',
        'escudo_casa': 'https://media.santosfc.com.br/wp-content/uploads/2022/04/cropped-Asset-2.png',
        'escudo_fora': 'https://upload.wikimedia.org/wikipedia/pt/thumb/8/8b/EscudoDoVascoDaGama.svg/950px-EscudoDoVascoDaGama.svg.png',
        'ingressos': 0,
        'preco': 35.00,
        'prevenda': False
    }
}

vendas = []
usuarios = {}
clientes_online = {}  # Rastrear clientes e suas ações
timers_prevenda = {}

def atualizar_timer(jogo_id, tempo_restante):
    """Atualiza timer a cada segundo via Socket.IO"""
    if tempo_restante > 0 and jogo_id in jogos and jogos[jogo_id]['prevenda']:
        socketio.emit('tick_timer', {'id': jogo_id, 'tempo': tempo_restante})
        timer = threading.Timer(1.0, atualizar_timer, args=[jogo_id, tempo_restante - 1])
        timer.start()
        timers_prevenda[jogo_id] = timer
    else:
        finalizar_prevenda(jogo_id)

def finalizar_prevenda(jogo_id):
    """Finaliza pré-venda"""
    if jogo_id in jogos:
        jogos[jogo_id]['prevenda'] = False
        socketio.emit('atualizar_jogo', {'id': jogo_id, 'jogo': jogos[jogo_id]})
        socketio.emit('prevenda_finalizada', {'id': jogo_id})
        print(f'Pré-venda finalizada para jogo {jogo_id}')

@app.route('/')
def index():
    return render_template('ingressos.html')

@socketio.on('connect')
def conectar():
    usuarios[request.sid] = {'tipo': None, 'nome': None}
    emit('inicio', {'jogos': jogos, 'vendas': vendas[-8:]})
    socketio.emit('online', len(usuarios))

@socketio.on('disconnect')
def desconectar():
    if request.sid in usuarios:
        if request.sid in clientes_online:
            del clientes_online[request.sid]
            socketio.emit('atualizar_clientes', list(clientes_online.values()))
        del usuarios[request.sid]
    socketio.emit('online', len(usuarios))

@socketio.on('definir_usuario')
def definir_usuario(data):
    tipo = data['tipo']
    nome = data.get('nome', 'Anônimo')
    
    usuarios[request.sid] = {'tipo': tipo, 'nome': nome}
    
    if tipo == 'cliente':
        clientes_online[request.sid] = {
            'sid': request.sid,
            'nome': nome,
            'acao': 'Entrou no sistema',
            'hora': datetime.now().strftime('%H:%M:%S')
        }
        socketio.emit('atualizar_clientes', list(clientes_online.values()))
    
    emit('usuario_definido', {'tipo': tipo, 'nome': nome})

@socketio.on('acao_cliente')
def acao_cliente(data):
    if request.sid in clientes_online:
        clientes_online[request.sid]['acao'] = data['acao']
        clientes_online[request.sid]['hora'] = datetime.now().strftime('%H:%M:%S')
        socketio.emit('atualizar_clientes', list(clientes_online.values()))

@socketio.on('liberar')
def liberar(data):
    id_jogo = int(data['id'])
    qtd = int(data['qtd'])
    preco = float(data['preco'])
    
    if id_jogo in jogos:
        jogos[id_jogo]['ingressos'] += qtd
        jogos[id_jogo]['preco'] = preco
        jogos[id_jogo]['prevenda'] = True
        
        # Cancelar timer anterior se existir
        if id_jogo in timers_prevenda:
            timers_prevenda[id_jogo].cancel()
        
        # Iniciar contagem regressiva via Socket.IO
        socketio.emit('atualizar_jogo', {'id': id_jogo, 'jogo': jogos[id_jogo]})
        socketio.emit('prevenda_iniciada', {'id': id_jogo})
        
        # Começar timer de 10 segundos
        atualizar_timer(id_jogo, 10)
        
        emit('ok', f'✅ {qtd} ingressos liberados! Pré-venda ativa por 10 segundos!')

@socketio.on('comprar')
def comprar(data):
    id_jogo = int(data['id'])
    qtd = int(data['qtd'])
    nome = data['nome']
    
    jogo = jogos.get(id_jogo)
    
    if not jogo or jogo['ingressos'] < qtd:
        emit('erro', '❌ Ingressos insuficientes!')
        return
    
    jogo['ingressos'] -= qtd
    
    # Calcular preço (10% desconto na pré-venda)
    preco_base = jogo['preco']
    if jogo['prevenda']:
        preco_final = preco_base * 0.9  # 10% de desconto
        tipo_venda = 'PRÉ-VENDA'
    else:
        preco_final = preco_base
        tipo_venda = 'NORMAL'
    
    valor = preco_final * qtd
    
    venda = {
        'id': len(vendas) + 1,
        'nome': nome,
        'jogo': f"{jogo['casa']} x {jogo['fora']}",
        'qtd': qtd,
        'valor': valor,
        'tipo': tipo_venda,
        'desconto': jogo['prevenda'],
        'hora': datetime.now().strftime('%H:%M:%S')
    }
    
    vendas.append(venda)
    
    # Atualizar ação do cliente
    if request.sid in clientes_online:
        clientes_online[request.sid]['acao'] = f'Comprou {qtd}x {jogo["casa"]} x {jogo["fora"]}'
        clientes_online[request.sid]['hora'] = datetime.now().strftime('%H:%M:%S')
        socketio.emit('atualizar_clientes', list(clientes_online.values()))
    
    socketio.emit('atualizar_jogo', {'id': id_jogo, 'jogo': jogo})
    socketio.emit('nova_venda', venda)
    
    msg = f'✅ Compra confirmada! R$ {valor:.2f}'
    if jogo['prevenda']:
        msg += ' (PRÉ-VENDA -10%)'
    
    emit('ok', msg)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)