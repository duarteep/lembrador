"""Funções utilitárias para o agendador de consultas."""
from datetime import datetime
import re


def validar_cpf(cpf):
    """Valida formato básico de CPF."""
    cpf_limpo = re.sub(r'\D', '', cpf)
    return len(cpf_limpo) == 11


def validar_email(email):
    """Valida formato básico de email."""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None


def validar_telefone(telefone):
    """Valida formato básico de telefone."""
    telefone_limpo = re.sub(r'\D', '', telefone)
    return len(telefone_limpo) >= 10


def formatar_data_hora(data_hora):
    """Formata data/hora para exibição."""
    if isinstance(data_hora, str):
        data_hora = datetime.fromisoformat(data_hora)
    return data_hora.strftime("%d/%m/%Y às %H:%M")


def formatar_telefone(telefone):
    """Formata telefone para exibição."""
    telefone_limpo = re.sub(r'\D', '', telefone)
    if len(telefone_limpo) == 11:
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
    elif len(telefone_limpo) == 10:
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
    return telefone


def formatar_cpf(cpf):
    """Formata CPF para exibição."""
    cpf_limpo = re.sub(r'\D', '', cpf)
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf


def validar_data_hora(data_str):
    """Valida e converte string de data/hora para datetime."""
    formatos = [
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d"
    ]
    
    for formato in formatos:
        try:
            data = datetime.strptime(data_str, formato)
            # Se apenas data foi fornecida, assume horário padrão
            if ":" not in data_str:
                data = data.replace(hour=14)  # Padrão: 14:00
            return data
        except ValueError:
            continue
    
    return None


def limpar_tela():
    """Limpa a tela do console."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_menu(opcoes):
    """Exibe um menu e retorna a opção selecionada."""
    print("\n" + "="*50)
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")
    print("="*50)
    
    while True:
        try:
            escolha = int(input("Escolha uma opção: "))
            if 1 <= escolha <= len(opcoes):
                return escolha
            print("Opção inválida!")
        except ValueError:
            print("Digite um número válido!")


def entrada_segura(mensagem, tipo=str, validador=None):
    """Obtém entrada do usuário com validação."""
    while True:
        try:
            valor = input(f"{mensagem}: ").strip()
            
            if not valor:
                print("Campo obrigatório!")
                continue
            
            if tipo == int:
                valor = int(valor)
            
            if validador and not validador(valor):
                print("Valor inválido!")
                continue
            
            return valor
        except ValueError:
            print(f"Digite um {tipo.__name__} válido!")
