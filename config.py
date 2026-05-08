"""Arquivo de configuração da aplicação."""
import os

# Banco de dados
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_NAME = "agendador"
DATABASE_USER = "your_username"
DATABASE_PASSWORD = "your_password"
DATABASE_SUPABASE_URL = os.environ.get('DATABASE_SUPABASE_URL')
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')

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
