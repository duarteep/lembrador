# 🚀 Agendador de Consultas - Início Rápido

## ⏱️ Comece em 3 passos

### 1️⃣ Instale as Dependências
```bash
pip install -r requirements-web.txt
```

### 2️⃣ Execute a Aplicação
```bash
python app.py
```

### 3️⃣ Abra no Navegador
Acesse: **http://localhost:5000**

---

## 🎯 Seu Primeiro Agendamento

### Passo 1: Cadastre um Paciente
- Clique em **Pacientes** → **Novo Paciente**
- Preencha os dados (Nome, CPF, Telefone, Email)
- Clique em **Salvar**

### Passo 2: Cadastre um Profissional
- Clique em **Profissionais** → **Novo Profissional**
- Preencha os dados (Nome, Especialidade, CRM, Telefone)
- Clique em **Salvar**

### Passo 3: Agende uma Consulta
- Clique em **Consultas** → **Agendar Consulta**
- Busque o paciente (CPF)
- Selecione especialidade
- Escolha o profissional
- Defina data/hora
- Clique em **Agendar**

---

## 📱 Interface Web

| Página | URL | Função |
|--------|-----|--------|
| Home | `/` | Dashboard com stats |
| Pacientes | `/pacientes` | Lista pacientes |
| Novo Paciente | `/pacientes/novo` | Cadastro |
| Profissionais | `/profissionais` | Lista profissionais |
| Novo Profissional | `/profissionais/novo` | Cadastro |
| Consultas | `/consultas` | Lista consultas |
| Agendar | `/consultas/nova` | Novo agendamento |

---

## 🛠️ Troubleshooting

**Porta já em uso?**
```bash
python -c "from app import app; app.run(port=5001)"
```

**Flask não encontrado?**
```bash
pip install Flask==2.3.3
```

**Banco corrompido?**
```bash
rm agendador.db  # Linux/Mac
del agendador.db # Windows
```

---

## 📖 Documentação

- **README.md** - Documentação completa
- **README-WEB.md** - Guia detalhado da web
- **GUIA_WEB.md** - Quick start 5 minutos

---

**Pronto para começar!** 🎉

