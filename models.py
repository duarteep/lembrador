"""Modelos de dados para o agendador de consultas."""
from datetime import datetime
from uuid import uuid4
from enum import Enum


class StatusConsulta(Enum):
    """Estados possíveis de uma consulta."""
    AGENDADA = "agendada"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    REALIZADA = "realizada"


class Paciente:
    """Representa um paciente no sistema."""

    def __init__(self, nome, cpf, telefone, email=None, id=None, preferencia_comunicacao='whatsapp'):
        self.id = id or str(uuid4())
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.preferencia_comunicacao = preferencia_comunicacao
        self.data_criacao = datetime.now()

    def __repr__(self):
        return f"Paciente(id={self.id}, nome={self.nome}, cpf={self.cpf}, telefone={self.telefone}, preferencia_comunicacao={self.preferencia_comunicacao})"


class Notificacao:
    """Representa uma notificação agendada no sistema."""

    def __init__(self, consulta_id, tipo, ferramenta, agendamento, titulo, descricao, status='agendada', id=None):
        self.id = id or str(uuid4())
        self.consulta_id = consulta_id
        self.tipo = tipo # automatica, manual
        self.ferramenta = ferramenta # sms, email, whatsapp, telegram
        self.agendamento = agendamento # datetime
        self.titulo = titulo
        self.descricao = descricao
        self.status = status # agendada, enviada, falha, cancelada
        self.data_criacao = datetime.now()

    def __repr__(self):
        return f"Notificacao(id={self.id}, consulta_id={self.consulta_id}, tipo={self.tipo}, ferramenta={self.ferramenta}, status={self.status})"

class Profissional:
    """Representa um profissional de saúde no sistema."""
    
    def __init__(self, nome, especialidade, crm, telefone, id=None):
        self.id = id or str(uuid4())
        self.nome = nome
        self.especialidade = especialidade
        self.crm = crm
        self.telefone = telefone
        self.data_criacao = datetime.now()
    
    def __repr__(self):
        return f"Profissional(id={self.id}, nome={self.nome}, especialidade={self.especialidade}, crm={self.crm})"


class Consulta:
    """Representa uma consulta agendada no sistema."""
    
    def __init__(self, paciente_id, profissional_id, data_hora, motivo, status=StatusConsulta.AGENDADA, id=None):
        self.id = id or str(uuid4())
        self.paciente_id = paciente_id
        self.profissional_id = profissional_id
        self.data_hora = datetime.fromisoformat(data_hora) if isinstance(data_hora, str) else data_hora
        self.motivo = motivo
        self.status = status if isinstance(status, StatusConsulta) else StatusConsulta(status)
        self.data_criacao = datetime.now()
        self.notas = ""
    
    def __repr__(self):
        return f"Consulta(id={self.id}, paciente_id={self.paciente_id}, profissional_id={self.profissional_id}, data_hora={self.data_hora}, status={self.status.value})"
    
    def atualizar_status(self, novo_status):
        """Atualiza o status da consulta."""
        if isinstance(novo_status, str):
            self.status = StatusConsulta(novo_status)
        else:
            self.status = novo_status
