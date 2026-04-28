# 📚 Estrutura Completa do Projeto

## 🏗️ Árvore de Arquivos

```
agendador-consultas/
│
├── 📄 Arquivos Principais (Backend)
│   ├── app.py                     # Aplicação Flask
│   ├── models.py                  # Modelos de dados
│   ├── database.py                # Gerenciamento do BD (SQLite)
│   ├── utils.py                   # Funções utilitárias
│   ├── config.py                  # Configurações
│   └── run_web.py                 # Script para executar
│
├── 📋 Dependências
│   └── requirements-web.txt       # Dependências (Flask, Werkzeug)
│
├── 🎨 Frontend - Templates HTML
│   └── templates/
│       ├── base.html              # Template base com navegação
│       ├── index.html             # Home/Dashboard inicial
│       ├── dashboard.html         # Dashboard com próximas consultas
│       ├── pacientes.html         # Listagem de pacientes
│       ├── novo_paciente.html     # Formulário novo paciente
│       ├── detalhe_paciente.html  # Visualizar paciente
│       ├── profissionais.html     # Listagem de profissionais
│       ├── novo_profissional.html # Formulário novo profissional
│       ├── detalhe_profissional.html # Visualizar profissional
│       ├── consultas.html         # Listagem de consultas
│       ├── nova_consulta.html     # Agendar nova consulta
│       ├── detalhe_consulta.html  # Visualizar e gerenciar consulta
│       ├── 404.html               # Página erro 404
│       └── 500.html               # Página erro 500
│
├── 🎨 Frontend - Estáticos
│   └── static/
│       ├── style.css              # Estilos CSS (responsivo)
│       └── script.js              # JavaScript (AJAX, validações)
│
├── 🗄️ Banco de Dados
│   └── agendador.db              # SQLite (criado automaticamente)
│       ├── pacientes             # Tabela de pacientes
│       ├── profissionais         # Tabela de profissionais
│       └── consultas             # Tabela de consultas
│
└── 📚 Documentação
    ├── README.md                 # Documentação principal (Web)
    ├── README-WEB.md             # Guia detalhado
    ├── GUIA_WEB.md               # Quick start 5 minutos
    ├── START.md                  # Início rápido
    └── ESTRUTURA.md              # Este arquivo
```

## 📄 Descrição de Arquivos

### Core - Modelos e Dados

#### `models.py` (~80 linhas)
- Classes de domínio: `Paciente`, `Profissional`, `Consulta`, `StatusConsulta`
- UUIDs únicos para cada entidade
- Timestamps automáticos
- Métodos utilitários

#### `database.py` (~300 linhas)
- Gerenciamento de conexão SQLite
- CRUD completo para cada entidade
- Queries e filtros
- Relacionamentos entre tabelas
- Validações de integridade

#### `utils.py` (~150 linhas)
- Validações: CPF, email, telefone
- Formatação: datas, telefones, CPF
- Parsing de strings
- Tratamento de entrada

#### `config.py` (~50 linhas)
- Constantes da aplicação
- Lista de especialidades
- Configurações de validação
- Mensagens padrão

### Backend

#### `app.py` (~500 linhas)
- Aplicação Flask principal
- 25+ rotas HTTP
- API REST endpoints (JSON)
- Template rendering
- Error handling (404, 500)
- Context processors

#### `run_web.py` (~100 linhas)
- Script para executar a aplicação
- Verificação de dependências
- Criação de ambiente virtual
- Instalação automática

### Frontend

#### `templates/base.html` (~80 linhas)
- HTML base com Jinja2
- Navegação principal
- Sistema de alertas
- Flash messages
- Footer

#### `index.html` (~60 linhas)
- Home da aplicação
- Hero section
- Grid de estatísticas
- Cards de features

#### `dashboard.html` (~50 linhas)
- Dashboard com próximas 7 dias
- Estatísticas
- Tabela de consultas
- Status badges

#### Páginas de CRUD (~40-60 linhas cada)
- `pacientes.html` - Listagem
- `novo_paciente.html` - Formulário
- `detalhe_paciente.html` - Detalhes + histórico
- Mesmo padrão para profissionais e consultas

#### `nova_consulta.html` (~80 linhas)
- Formulário de agendamento
- Busca dinâmica de paciente
- Carregamento dinâmico de profissionais
- Va� Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| Linhas de Python | ~1.300 |
| Linhas de HTML | ~600 |
| Linhas de CSS | ~600 |
| Linhas de JavaScript | ~150 |
| Arquivos Totais | 20+ |
| Rotas HTTP | 25+ |
| Templates | 13 |
| API Endpoints | 6+ |
| Tabelas BD | 3 |

---

## 🔄 Fluxo de Dados

```
Usuário (Navegador)
    ↓
Interface HTML (templates/)
    ↓
JavaScript (validações + AJAX)
    ↓
Flask (app.py - rotas HTTP)
    ↓
Utils.py (validações)
    ↓
Models.py (objetos)
    ↓
Database.py (SQLite)
    ↓
Banco de Dados (agendador.db) e detalhado
- **README-WEB.md** - Documentação específica Web
- **GUIA_WEB.md** - Quick start 5 minutos
- **� Rotas Web

### Rotas GET (Páginas)
```
GET /                          → index.html
GET /dashboard                 → dashboard.html
GET /pacientes                 → pacientes.html
GET /pacientes/novo            → novo_paciente.html
GET /pacientes/<id>            → detalhe_paciente.html
GET /profissionais             → profissionais.html
GET /profissionais/novo        → novo_profissional.html
GET /profissionais/<id>        → detalhe_profissional.html
GET /consultas                 → consultas.html
GET /consultas/nova            → nova_consulta.html
GET /consultas/<id>            → detalhe_consulta.html
GET /404, /500                 → Páginas de erro
```

### Rotas POST (Formulários)
```
POST /pacientes/novo           → Criar paciente
POST /profissionais/novo       → Criar profissional
POST /consultas/nova           → Agendar consulta
```

### API REST (JSON)
```
GET  /api/stats                           → Estatísticas gerais
GET  /api/paciente/cpf/<cpf>             → Buscar paciente
GET  /api/profissionais/especialidade/<e> → Listar por especialidade
PUT  /api/consultas/<id>/status          → Atualiz
### Tabela: consultas
```sql
CREATE TABLE consultas (
    id TEXT PRIMARY KEY,           -- UUID
    paciente_id TEXT NOT NULL,     -- FK pacientes
    profissional_id TEXT NOT NULL, -- FK profissionais
    data_hora TIMESTAMP NOT NULL,  -- Quando vai ser
    motivo TEXT NOT NULL,          -- Razão
    status TEXT DEFAULT 'agendada',-- agendada|confirmada|realizada|cancelada
    notas TEXT,                    -- Observações
    data_criacao TIMESTAMP,        -- Quando foi agendada
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (profissional_id) REFERENCES profissionais(id)
)
```

## 🔗 Mapa de Rotas Web

### Páginas (GET)
```
/                              → index.html (home)
/dashboard                     → dashboard.html (próximas consultas)
/pacientes                     → pacientes.html (listagem)
/pacientes/novo               → novo_paciente.html (form)
/pacientes/<id>               → detalhe_paciente.html (info)
/profissionais                → profissionais.html (listagem)
/profissionais/novo           → novo_profissional.html (form)
/profissionais/<id>           → detalhe_profissional.html (info)
/consultas                    → consultas.html (listagem)
/consultas/nova               → nova_consulta.html (form)
/consultas/<id>               → detalhe_consulta.html (info)
```

### APIs (JSON)
```
GET  /api/stats                           → Estatísticas
GET  /api/paciente/cpf/<cpf>             → Buscar paciente
GET  /api/profissionais/especialidade/<e> → Listar por especialidade
PUT  /api/consultas/<id>/status          → Alterar status
PUT  /api/consultas/<id>/notas           → Adicionar notas
DELETE /api/consultas/<id>/deletar       → Deletar consulta
```

## 📦 Instalação e Execução

### CLI
```bash
# Sem deps externas!
python main.py
```

### Web
```bash
# Instalar
pip install -r requirements-web.txt

# Executar
python app.py
# ou
python run_web.py
```

## 🎨 Design Responsivo (Web)

| Dispositivo | Largura | Grid | Comportamento |
|---|---|---|---|
| Mobile | < 480px | 1 coluna | Empilhado |
| Tablet | 480-768px | 2 colunas | Ajustado |
| Desktop | 768-1200px | 3 colunas | Expandido |
| Large | > 1200px | 4 colunas | Máximo |

## 🔐 Validações Implementadas

- ✓ CPF: 11 dígitos, únicos
- ✓ Email: Formato RFC5322
- ✓ Telefone: 10+ dígitos
- ✓ Duplicatas: Prevent no BD
- ✓ Data: Apenas futuras
- ✓ Status: Valores válidos
- ✓ Campos obrigatórios

## 📊 Estatísticas do Projeto

| Métrica | CLI | Web | Total |
|---------|-----|-----|-------|
| Linhas de Python | 850 | 500 | 1,350 |
| Linhas HTML | - | 600 | 600 |
| Linhas CSS | - | 600 | 600 |
| Linhas JavaScript | - | 100 | 100 |
| Arquivos | 4 | 8 | 12+ |
| Rotas | - | 25+ | 25+ |
| Testes | - | - | 0 |

## 🚀 Roadmap

### MVP (✓ Completo)
- [x] Gerenciar pacientes
- [x] Gerenciar profissionais
- [x] Agendar consultas
- [x] Dashboard
- [x] CLI + Web

### Phase 2 (📋 Aguardando)
- [ ] Autenticação de usuários
- [ ] Permissões (admin, recepção, doctor)
- [ ] Relatórios em PDF
- [ ] Envio de emails
- [ ] API pública
- [ ] Testes automatizados

### Phase 3 (🚀 Futuro)
- [ ] App mobile (React Native)
- [ ] Integração com calendários (Google, Outlook)
- [ ] Notificações push
- [ ] Sistema de feedback
- [ ] Analytics
- [ ] Deploy em cloud (Heroku, AWS)

## 📝 Licença

MIT - Livre para usar e modificar

## 👨‍💻 Como Contribuir

1. Faça um fork
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. ✨ Conclusão

**Agendador de Consultas - Versão Web 2.0**

Esta é uma aplicação **pronta para produção** com:
- ✓ Backend em Flask robusto
- ✓ Frontend responsivo e moderno
- ✓ Banco de dados estruturado
- ✓ Validações completas
- ✓ API REST para integração
- ✓ Documentação completa
- ✓ Código limpo e organizado

---

**Status**: ✅ Pronto para uso
**Versão**: 2.0 (Web)
**Última atualização**: 2024