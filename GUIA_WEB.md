# 🚀 Guia de Início Rápido - Versão Web

## Instalação em 5 minutos

### Step 1️⃣: Instalar Dependências
```bash
pip install -r requirements-web.txt
```

### Step 2️⃣: Executar a Aplicação
```bash
python app.py
```

### Step 3️⃣: Abrir no Navegador
Acesse: **http://localhost:5000**

---

## ✨ Seu Primeiro Agendamento

### 1. Adicione um Paciente
- Clique em **Pacientes** → **Novo Paciente**
- Preencha os dados
- Clique em **Salvar**

### 2. Adicione um Profissional
- Clique em **Profissionais** → **Novo Profissional**
- Preencha os dados
- Clique em **Salvar**

### 3. Agende uma Consulta
- Clique em **Consultas** → **Agendar Consulta**
- Busque o paciente (CPF)
- Selecione especialidade
- Escolha o profissional
- Defina data/hora
- Clique em **Agendar**

---

## 🎯 Funções Principais

| Função | Caminho | Ícone |
|--------|---------|-------|
| Home | `/` | 🏠 |
| Dashboard | `/dashboard` | 📊 |
| Listar Pacientes | `/pacientes` | 👥 |
| Novo Paciente | `/pacientes/novo` | ➕ |
| Listar Profissionais | `/profissionais` | 👨‍⚕️ |
| Novo Profissional | `/profissionais/novo` | ➕ |
| Listar Consultas | `/consultas` | 📋 |
| Agendar Consulta | `/consultas/nova` | 📅 |

---

## 📝 Dados de Teste

### Paciente Exemplo
```
Nome: João Silva
CPF: 12345678901
Telefone: 11987654321
Email: joao@email.com
```

### Profissional Exemplo
```
Nome: Dra. Maria Santos
Especialidade: Cardiologia
CRM: 123456/SP
Telefone: 1133334444
```

---

## 🛠️ Troubleshooting

### Problema: "Address already in use"
Use outra porta:
```bash
python -c "from app import app; app.run(port=5001)"
```

### Problema: "ModuleNotFoundError: No module named 'flask'"
Reinstale as dependências:
```bash
pip install --upgrade -r requirements-web.txt
```

### Problema: Banco de dados corrompido
Delete e recrie:
```bash
del agendador.db
python app.py
```

---

## 📱 Compatibilidade

✅ Chrome/Edge (recomendado)
✅ Firefox
✅ Safari
✅ Mobile browsers

---

## 💡 Dicas

- **Busca Automática**: Ao digitar CPF, clique no ícone 🔍 para buscar
- **Carregamento de Profissionais**: Ao selecionar especialidade, os profissionais aparecem automaticamente
- **Data Mínima**: Consultas só podem ser agendadas para amanhã ou depois
- **Status**: Você pode mudar o status da consulta em detalhes

---

## 📞 Suporte

Dúvidas? Verifique o arquivo **README-WEB.md** para documentação completa.

**Pronto para começar!** 🎉
