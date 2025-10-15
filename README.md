<div align="center">

# ⚽ Sistema de Venda de Ingressos

### Sistema de vendas em tempo real com Socket.IO

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-5.3.5-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://socket.io/)

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%" />

</div>

## 📋 Sobre o Projeto

Sistema de venda de ingressos para jogos de futebol com comunicação em tempo real usando Socket.IO. Possui pré-venda com **10% de desconto** nos primeiros **10 segundos** após liberação dos ingressos.

### ✨ Principais Funcionalidades

- ⚡ Atualizações em tempo real via Socket.IO
- ⏰ Pré-venda com 10% de desconto (10 segundos)
- 🎯 Timer sincronizado entre todos os usuários
- 🛡️ Escudos oficiais dos times brasileiros

---

## 🚀 Tecnologias Utilizadas

- **Backend:** Flask + Socket.IO
- **Frontend:** HTML, CSS, JavaScript
- **Comunicação:** WebSockets em tempo real

---

## 📦 Instalação

### Clone o repositório
```bash
git clone https://github.com/Luiz-beto/Venda-de-ingressos.git
cd Venda-de-ingressos
```

### Instale as dependências
```bash
pip install -r requirements.txt
```

### Execute o servidor
```bash
python app.py
```

### Acesse no navegador
```
http://localhost:5000
```

---

## 💻 Como Usar

### 👨‍💼 Administrador
1. Clique em **ADMINISTRADOR**
2. Escolha o jogo e defina preço/quantidade
3. Clique em **LIBERAR INGRESSOS**
4. Pré-venda inicia automaticamente por 10 segundos

### 🎫 Cliente
1. Clique em **CLIENTE**
2. Veja os jogos disponíveis
3. Durante a pré-venda: **10% de desconto** + timer regressivo
4. Compre seus ingressos em tempo real

---

## ⏰ Sistema de Pré-venda

Quando o admin libera ingressos:
- ✅ Pré-venda ativa por **10 segundos**
- ✅ Timer sincronizado: `10s → 9s → 8s...`
- ✅ **10% de desconto** no preço
- ✅ Após 10s, preço volta ao normal

**Exemplo:**
- Preço normal: R$ 50,00
- Pré-venda: R$ 45,00 (economia de R$ 5,00)

---

## 🏟️ Jogos Disponíveis

| Jogo | Preço |
|------|-------|
| Flamengo x Palmeiras | R$ 50,00 |
| Corinthians x São Paulo | R$ 45,00 |
| Grêmio x Internacional | R$ 40,00 |
| Santos x Vasco | R$ 35,00 |

---

## 🧪 Testando

**Abra 2 abas do navegador:**
1. **Aba 1:** Entre como ADMIN e libere ingressos
2. **Aba 2:** Entre como CLIENTE e veja o timer sincronizado
3. Compre durante a pré-venda com desconto!

---

## 📂 Estrutura
```
venda-ingressos/
├── app.py                 # Servidor Flask + Socket.IO
├── requirements.txt       # Dependências
└── templates/
    └── index.html        # Interface
```

---

## 🔌 Eventos Socket.IO

**Servidor → Cliente:**
- `tick_timer` - Contagem regressiva (10, 9, 8...)
- `atualizar_jogo` - Atualiza disponibilidade
- `nova_venda` - Notifica nova compra

**Cliente → Servidor:**
- `liberar` - Libera ingressos (admin)
- `comprar` - Compra ingressos (cliente)

---

## 📚 Dependências
```txt
Flask==3.0.0
Flask-SocketIO==5.3.5
python-socketio==5.10.0
```

---

## 👨‍💻 Autor

**Luiz Roberto Sardanha**  
Estudante de Sistemas de Informação  
Unidavi - Rio do Sul, SC

**Professor Orientador:** Ademar Perfoll Junior

---

<div align="center">

**Sistema de Venda de Ingressos** | Flask + Socket.IO | 2025

⚽ Desenvolvido para demonstrar comunicação em tempo real

</div>