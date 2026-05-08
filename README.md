# 🌐 Agendador de Consultas - Versão Web

Uma aplicação web moderna para gerenciar agendamento de consultas médicas/odontológicas, desenvolvida com **Flask**.

## 🚀 Funcionalidades

- ✅ **Interface Web Moderna**: Design responsivo e intuitivo
- ✅ **Gerenciamento de Pacientes**: Cadastro, listagem e consulta com CPF
- ✅ **Gerenciamento de Profissionais**: Cadastro por especialidade
- ✅ **Agendamento de Consultas**: Sistema completo com data/hora
- ✅ **Dashboard**: Consultas próximas dos próximos 7 dias
- ✅ **Gerenciamento de Status**: Alterar entre agendada, confirmada, realizada, cancelada
- ✅ **Notas e Observações**: Adicionar informações às consultas
- ✅ **API REST**: Endpoints JSON para integração
- ✅ **Responsivo**: Funciona em Desktop, Tablet e Smartphone
- ✅ **Persistência de Dados**: Banco de dados PostgreSQL

## 📋 Requisitos

- Python 3.7+
- Flask 2.3.3+
- Werkzeug 2.3.7+

## 🔧 Instalação

### 1. Clone o repositório ou extraia os arquivos

```bash
cd lembrador
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### 1. Executar a aplicação

```bash
python app.py
```

Acesse no navegador: **http://localhost:5000**

### 2. Navegação Web

A aplicação web fornece uma interface intuitiva com menu de navegação:

- **Home**: Visão geral com estatísticas
- **Dashboard**: Próximas consultas (7 dias)
- **Pacientes**: Listar, criar e visualizar pacientes
- **Profissionais**: Listar, criar e visualizar profissionais
- **Consultas**: Listar, agendar e gerenciar consultas

### 3. Fluxo de Uso Típico

#### 1️⃣ Cadastrar Paciente
- Clique em **Pacientes** → **Novo Paciente**
- Preencha: Nome, CPF, Telefone, Email (opcional)
- Clique em **Salvar**

#### 2️⃣ Cadastrar Profissional
- Clique em **Profissionais** → **Novo Profissional**
- Preencha: Nome, Especialidade, CRM, Telefone
- Clique em **Salvar**

#### 3️⃣ Agendar Consulta
- Clique em **Consultas** → **Agendar Consulta**
- Digite o CPF do paciente (clique em 🔍 para buscar)
- Informe a especialidade desejada
- Selecione o profissional
- Escolha a data e hora
- Descreva o motivo
- Clique em **Agendar**

#### 4️⃣ Gerenciar Consultas
- Clique em **Consultas** para ver lista completa
- Clique em **Ver Detalhes** para:
  - Alterar status
  - Adicionar notas
  - Cancelar consulta
  - Deletar (se necessário)

### 4. Executar o Scheduler de Notificações (Opcional)

```bash
python notificacao_scheduler.py
```

Este script roda em background verificando notificações pendentes a cada 15 minutos e enviando via WhatsApp automaticamente. Notificações vencidas há mais de 30 minutos são automaticamente marcadas como falha para evitar spam. As mensagens incluem detalhes completos da consulta (data, horário, profissional, especialidade, status).

## 📁 Estrutura do Projeto

```
agendador-consultas/
├── app.py                       # Aplicação Flask
├── models.py                    # Classes de dados (Paciente, Profissional, Consulta)
├── database.py                  # Gerenciamento do banco de dados
├── utils.py                     # Funções utilitárias
├── config.py                    # Configurações
├── requirements.txt         # Dependências
├── PostgreSQL                  # Banco de dados configurado em config.py ou DATABASE_SUPABASE_URL
├── templates/                   # Templates HTML
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
├── static/
│   ├── style.css                # Estilos CSS responsivos
│   └── script.js                # JavaScript
└── README.md         
## 📊 Modelos de Dados

### Paciente
- ID (UUID)
- Nome
- CPF (único)
- Telefone
- Email (opcional)
- Data de criação

### Profissional, previne duplicatas
- ✅ **Email**: Valida formato RFC5322
- ✅ **Telefone**: Requer mínimo 10 dígitos
- ✅ **CRM**: Único por profissional
- ✅ **Data/Hora**: Apenas datas futuras
- ✅ **Status**: Valores pré-definidos
- ✅ **Campos Obrigatórios**: Validação cliente e servidor

## 🔐 Formatação de Dados

A aplicação trata automaticamente:
- **CPF**: 123.456.789-01
- **Telefone**: (11) 98765-4321 ou (11) 3456-7890
- **Data/Hora**: 25/12/2024 às 14:30

## 💾 Banco de Dados

A aplicação utiliza PostgreSQL, com conexão configurada em `config.py` ou pela variável de ambiente `DATABASE_SUPABASE_URL`.

### Tabelas:
- `pacientes` - Armazena informações de pacientes
- `profissionais` - Armazena profissionais de saúde
- `consultas` - Armazena agendamentos com status

## 🔄 Fluxo de Agendamento

```
1. Cadastrar Paciente (CPF único)
   ↓
2. Cadastrar Profissional (especialidade + CRM)
   ↓
3. Agendar Consulta
   ├─ Buscar Paciente por CPF
   ├─ Selecionar Especialidade
   ├─ Escolher Profissional
   ├─ Definir Data/Hora (futura)
   └─ Descrever Motivo
   ↓
4. Consulta criada com status "AGENDADA"
   ├─ Pode alterar para "CONFIRMADA"
   ├─ Pode alterar para "REALIZADA"
   └─ Pode alterar para "CANCELADA"
```

## 🗺️ API REST Endpoints

A aplicação fornece endpoints JSON para integração:

- `GET /api/stats` - Estatísticas gerais
- `GET /api/paciente/cpf/<cpf>` - Buscar paciente por CPF
- `GET /api/profissionais/especialidade/<esp>` - Listar profissionais
- `PUT /api/consultas/<id>/status` - Alterar status
- `PUT /api/consultas/<id>/notas` - Adicionar notas
- `DELETE /api/consultas/<id>/deletar` - Deletar consulta

## 🔄 Fluxo de Agendamento

```
1. Selecionar Paciente (por CPF)
2. Selecionar Especialidade
3. Escolher Profissional
4. Informar o motivo
```bash
pip install -r requirements.txt
```

### Erro: "Address already in use"
A porta 5000 já está em uso. Use outra porta no código:
```python
app.run(port=5001)
```

### Erro: "CPF já cadastrado"
Este CPF já existe no sistema. Use outro ou consulte o paciente existente.

### Erro: "Data/hora inválida"
A data deve ser futura. Escolha uma data e hora no futuro.

### Adicionar Paciente via Web
1. Navegue para: http://localhost:5000/pacientes/novo
2. Preencha o formulário
3. Clique em "Salvar"

### Adicionar Profissional via Web
1. Navegue para: http://localhost:5000/profissionais/novo
2. Preencha os dados
3. Clique em "Salvar"

### Agendar Consulta via Web
1. Navegue para: http://localhost:5000/consultas/nova
2. Digite CPF do paciente (clique em 🔍 para buscar)
3. Selecione especialidade
4. Escolha profissional
5. Defina data/hora
6. Clique em "Agendar"

## 📱 Compatibilidade

- ✅ Chrome/Chromium (Recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Navegadores móveis

## 🌐 Deploy

### Localmente
```bash
python app.py
```
Acesse: http://localhost:5000

### Em Rede
```bash
python -c "from app import app; app.run(host='0.0.0.0', port=5000)"
```
Acesse: http://IP_DO_SERVIDOR:5000

### Em Produção (Heroku)
```bash
pip freeze > requirements.txt
heroku create seu-app
git push heroku main
```

## 🚀 Melhorias Futuras

- [ ] Autenticação de usuários
- [ ] Sistema de permissões
- [ ] Envio de lembretes por email
- [ ] Relatórios em PDF
- [ ] Integração com calendários
- [ ] Notificações push
- [ ] App mobile
- [x] Sistema de notificações automáticas via WhatsApp (notificacao_scheduler.py)

## 📄 Licença

Este projeto é fornecido como está, para uso livre.

## 👨‍💻 Desenvolvedor

Agendador de Consultas - Versão Web 2.0

---

**Versão**: 2.0 (Web)  
**Status**: Pronto para Produção ✅  
**Última atualização**: 2026

Para suporte ou dúvidas, revise a documentação do código ou adicione mais funcionalidades conforme necessário.
