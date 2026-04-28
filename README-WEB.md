# 🌐 Agendador de Consultas - Versão Web

Uma aplicação web moderna para gerenciar agendamento de consultas médicas/odontológicas, desenvolvida com Flask.

## 🚀 Características

### Frontend
- ✅ Interface responsiva e moderna
- ✅ Design limpo e intuitivo
- ✅ Navegação fácil
- ✅ Funcionalidades interativas com AJAX
- ✅ Suporte mobile

### Backend
- ✅ API RESTful completa
- ✅ Gerenciamento de pacientes, profissionais e consultas
- ✅ Validações robustas
- ✅ Banco de dados SQLite
- ✅ Tratamento de erros

## 📋 Funcionalidades

### Pacientes
- 👥 Cadastro com CPF, telefone, email
- 📋 Listagem completa
- 🔍 Busca por CPF
- 📊 Histórico de consultas

### Profissionais
- 👨‍⚕️ Cadastro com especialidade e CRM
- 📋 Listagem por especialidade
- 📞 Contato direto
- 📊 Agenda de consultas

### Consultas
- 📅 Agendamento com data/hora
- 🔄 Gerenciamento de status
- 📝 Notas e observações
- 🗑️ Exclusão segura
- ⏰ Próximas consultas

## 🔧 Instalação

### 1. Prerequisitos
- Python 3.7+
- pip (gerenciador de pacotes Python)

### 2. Clonar/Extrair Arquivos
```bash
cd agendador-consultas
```

### 3. Criar Ambiente Virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependências
```bash
pip install -r requirements-web.txt
```

### 5. Estrutura de Pastas Necessária
```
agendador-consultas/
├── app.py                  # Aplicação Flask
├── models.py              # Modelos de dados
├── database.py            # Banco de dados
├── utils.py               # Funções utilitárias
├── config.py              # Configurações
├── requirements-web.txt   # Dependências
├── templates/             # Arquivos HTML
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── pacientes.html
│   ├── novo_paciente.html
│   ├── detalhe_paciente.html
│   ├── profissionais.html
│   ├── novo_profissional.html
│   ├── detalhe_profissional.html
│   ├── consultas.html
│   ├── nova_consulta.html
│   ├── detalhe_consulta.html
│   ├── 404.html
│   └── 500.html
└── static/               # Arquivos estáticos
    ├── style.css        # Estilos
    └── script.js        # JavaScript
```

## 🎯 Como Executar

```bash
python app.py
```

Acesse no navegador: **http://localhost:5000**

## 🗺️ Mapa de Rotas

### Páginas Principais
- `/` - Home com statistics
- `/dashboard` - Dashboard com próximas consultas
- `/pacientes` - Listagem de pacientes
- `/pacientes/novo` - Adicionar novo paciente
- `/pacientes/<id>` - Detalhes do paciente
- `/profissionais` - Listagem de profissionais
- `/profissionais/novo` - Adicionar novo profissional
- `/profissionais/<id>` - Detalhes do profissional
- `/consultas` - Listagem de consultas
- `/consultas/nova` - Agendar nova consulta
- `/consultas/<id>` - Detalhes da consulta

### API Endpoints
- `GET /api/stats` - Estatísticas gerais
- `GET /api/paciente/cpf/<cpf>` - Obter paciente por CPF
- `GET /api/profissionais/especialidade/<esp>` - Profissionais por especialidade
- `PUT /api/consultas/<id>/status` - Atualizar status
- `PUT /api/consultas/<id>/notas` - Adicionar notas
- `DELETE /api/consultas/<id>/deletar` - Deletar consulta

## 💻 Uso da Aplicação

### 1️⃣ Cadastrar Paciente
1. Clique em "Pacientes" → "Novo Paciente"
2. Preencha os dados (Nome, CPF, Telefone, Email)
3. Clique em "Salvar"

### 2️⃣ Cadastrar Profissional
1. Clique em "Profissionais" → "Novo Profissional"
2. Preencha os dados (Nome, Especialidade, CRM, Telefone)
3. Clique em "Salvar"

### 3️⃣ Agendar Consulta
1. Clique em "Consultas" → "Agendar Consulta"
2. Digite o CPF do paciente (clique em 🔍 para buscar)
3. Informe a especialidade desejada
4. Selecione o profissional
5. Escolha data e hora
6. Descreva o motivo
7. Clique em "Agendar"

### 4️⃣ Gerenciar Consultas
- Ver próximas 7 dias no Dashboard
- Alterar status (Agendada → Confirmada → Realizada/Cancelada)
- Adicionar notas
- Deletar consulta se necessário

## 🎨 Interface

### Temas de Cores
- **Primário**: Azul (#3498db)
- **Sucesso**: Verde (#27ae60)
- **Perigo**: Vermelho (#e74c3c)
- **Aviso**: Laranja (#f39c12)

### Design Responsivo
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1200px)
- ✅ Mobile (até 768px)

## 🔐 Validações

A aplicação realiza validações robustas:
- ✅ CPF: 11 dígitos únicos
- ✅ Email: Formato válido
- ✅ Telefone: Mínimo 10 dígitos
- ✅ CRM: Campo único para profissionais
- ✅ Data/Hora: Não permite passado
- ✅ Duplicação: Prevent duplicate records

## 📦 Estrutura de Dados

### Pacientes
- ID (UUID)
- Nome
- CPF (único)
- Telefone
- Email (opcional)
- Data de criação

### Profissionais
- ID (UUID)
- Nome
- Especialidade
- CRM (único)
- Telefone
- Data de criação

### Consultas
- ID (UUID)
- Paciente ID
- Profissional ID
- Data/Hora
- Motivo
- Status (agendada, confirmada, realizada, cancelada)
- Notas
- Data de criação

## 🚀 Deploy

### Heroku
```bash
pip freeze > requirements.txt
heroku create seu-app-name
git push heroku main
```

### PythonAnywhere
1. Fazer upload dos arquivos
2. Configurar WSGI
3. Definir variáveis de ambiente

## 🐛 Troubleshooting

### Erro 404 - "Não encontrado"
- Verifique se a pasta `templates/` existe
- Verifique se os arquivos .html estão na pasta correta

### Erro "No module named 'flask'"
```bash
pip install -r requirements-web.txt
```

### Banco de dados corrompido
```bash
rm agendador.db
python app.py
```

### Porta 5000 já em uso
```bash
python app.py --port 5001
```

## 📝 Exemplos de Requisições

### Buscar Paciente por CPF
```bash
curl http://localhost:5000/api/paciente/cpf/12345678901
```

### Profissionais por Especialidade
```bash
curl http://localhost:5000/api/profissionais/especialidade/Cardiologia
```

### Atualizar Status da Consulta
```bash
curl -X PUT http://localhost:5000/api/consultas/ID/status \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmada"}'
```

## 🔄 Fluxo de Agendamento

```
┌─────────────┐
│  Homepage   │ (Dashboard)
└──────┬──────┘
       │
       ├─── Cadastra Paciente ───► Paciente criado
       │
       ├─── Cadastra Profissional ───► Profissional criado
       │
       └─── Agendar Consulta
            ├─ Busca Paciente
            ├─ Seleciona Especialidade
            ├─ Escolhe Profissional
            ├─ Define Data/Hora
            ├─ Descreve Motivo
            └─► Consulta "AGENDADA"
                ├─ Pode confirmar ───► "CONFIRMADA"
                ├─ Pode realizar ────► "REALIZADA"
                └─ Pode cancelar ────► "CANCELADA"
```

## 📊 Dashboard

O dashboard exibe:
- 📈 Total de pacientes
- 👥 Total de profissionais
- 📋 Total de consultas
- ⏰ Próximas consultas (7 dias)

## 🔔 Recursos Futuros

- [ ] Envio de emails/SMS para lembretes
- [ ] Autenticação de usuários
- [ ] Painel administrativo
- [ ] Relatórios em PDF
- [ ] Integração com calendários
- [ ] Sistema de feedback
- [ ] API pública (com token)
- [ ] Aplicativo mobile

## 📄 Licença

Este projeto é fornecido como está, para uso livre.

## 👨‍💻 Desenvolvedor

Agendador de Consultas - Versão Web 1.0

---

**Dica**: Para desenvolvimento, use modo debug ativado (já está em `app.py`):
```python
app.run(debug=True)
```

Para produção, desative:
```python
app.run(debug=False)
```

**Nota de Segurança**: Altere a `secret_key` em `app.py` antes de deployar em produção!
