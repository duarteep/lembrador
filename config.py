"""Arquivo de configuração da aplicação."""

# Banco de dados
DATABASE_NAME = "agendador.db"

# Especialidades comuns
ESPECIALIDADES = [
    "Cardiologia",
    "Dermatologia",
    "Ortopedia",
    "Pediatria",
    "Odontologia",
    "Oftalmologia",
    "Otorrinolaringologia",
    "Gastroenterologia",
    "Neurologia",
    "Psicologia",
    "Fisioterapia",
    "Nutrição"
]

# Estados de Consulta
STATUS_CONSULTA = {
    "agendada": "Agendada",
    "confirmada": "Confirmada",
    "realizada": "Realizada",
    "cancelada": "Cancelada"
}

# Configurações de data
FORMATO_DATA = "%d/%m/%Y"
FORMATO_DATA_HORA = "%d/%m/%Y %H:%M"
HORARIO_PADRAO = 14  # 14:00

# Configurações de validação
CPF_TAMANHO = 11
TELEFONE_TAMANHO_MIN = 10
TELEFONE_TAMANHO_MAX = 11

# Mensagens
MSG_SUCESSO = "✓"
MSG_ERRO = "✗"
MSG_ATENCAO = "⚠️"

# Cores para terminal (opcional)
CORES = {
    "verde": "\033[92m",
    "vermelho": "\033[91m",
    "amarelo": "\033[93m",
    "azul": "\033[94m",
    "reset": "\033[0m"
}
