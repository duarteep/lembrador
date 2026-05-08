"""Gerenciamento de banco de dados PostgreSQL para o agendador."""
import os
import psycopg2
from psycopg2 import IntegrityError
from config import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
)
from models import Paciente, Profissional, Consulta, StatusConsulta, Notificacao


class Database:
    """Gerencia a conexão e operações com o banco de dados PostgreSQL."""
    
    def __init__(self, DATABASE_SUPABASE_URL=None):
        self.DATABASE_SUPABASE_URL = DATABASE_SUPABASE_URL or os.environ.get('DATABASE_SUPABASE_URL')
        self.criar_tabelas()
    
    def _conectar(self):
        """Cria uma conexão com o banco de dados."""
        if self.DATABASE_SUPABASE_URL:
            return psycopg2.connect(self.DATABASE_SUPABASE_URL)

        return psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            dbname=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
        )
    
    def criar_tabelas(self):
        """Cria as tabelas do banco de dados se não existirem."""
        conn = self._conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT,
                preferencia_comunicacao TEXT DEFAULT 'whatsapp',
                data_criacao TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profissionais (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                especialidade TEXT NOT NULL,
                crm TEXT UNIQUE NOT NULL,
                telefone TEXT NOT NULL,
                data_criacao TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id TEXT PRIMARY KEY,
                paciente_id TEXT NOT NULL,
                profissional_id TEXT NOT NULL,
                data_hora TIMESTAMP NOT NULL,
                motivo TEXT NOT NULL,
                status TEXT DEFAULT 'agendada',
                notas TEXT,
                data_criacao TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY (profissional_id) REFERENCES profissionais(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notificacoes (
                id TEXT PRIMARY KEY,
                consulta_id TEXT NOT NULL,
                tipo TEXT NOT NULL,
                ferramenta TEXT NOT NULL,
                agendamento TIMESTAMP NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                status TEXT DEFAULT 'agendada',
                data_criacao TIMESTAMP,
                FOREIGN KEY (consulta_id) REFERENCES consultas(id)
            )
        """)
        
        conn.commit()
        conn.close()

    def limpar_banco(self):
        """Remove todas as tabelas e recria o esquema vazio."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS notificacoes, consultas, profissionais, pacientes CASCADE")
        conn.commit()
        conn.close()
        self.criar_tabelas()
    
    # ===== OPERAÇÕES COM PACIENTES =====
    
    def adicionar_paciente(self, paciente):
        """Adiciona um novo paciente ao banco de dados."""
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            cursor.execute(
                """
                    INSERT INTO pacientes (id, nome, cpf, telefone, email, data_criacao)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (paciente.id, paciente.nome, paciente.cpf, paciente.telefone, paciente.email, paciente.data_criacao),
            )
            conn.commit()
            conn.close()
            return True
        except IntegrityError as e:
            print(f"Erro: {e}")
            return False
    
    def obter_paciente(self, paciente_id):
        """Obtém um paciente pelo ID."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE id = %s", (paciente_id,))
        dados = cursor.fetchone()
        conn.close()
        
        if dados:
            return Paciente(dados[1], dados[2], dados[3], dados[4], dados[0])
        return None
    
    def obter_paciente_cpf(self, cpf):
        """Obtém um paciente pelo CPF."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE cpf = %s", (cpf,))
        dados = cursor.fetchone()
        conn.close()
        
        if dados:
            return Paciente(dados[1], dados[2], dados[3], dados[4], dados[0])
        return None
    
    def listar_pacientes(self):
        """Lista todos os pacientes."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes ORDER BY nome")
        dados = cursor.fetchall()
        conn.close()
        
        return [Paciente(d[1], d[2], d[3], d[4], d[0]) for d in dados]
    
    # ===== OPERAÇÕES COM PROFISSIONAIS =====
    
    def adicionar_profissional(self, profissional):
        """Adiciona um novo profissional ao banco de dados."""
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            cursor.execute(
                """
                    INSERT INTO profissionais (id, nome, especialidade, crm, telefone, data_criacao)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (profissional.id, profissional.nome, profissional.especialidade, profissional.crm, profissional.telefone, profissional.data_criacao),
            )
            conn.commit()
            conn.close()
            return True
        except IntegrityError as e:
            print(f"Erro: {e}")
            return False
    
    def obter_profissional(self, profissional_id):
        """Obtém um profissional pelo ID."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profissionais WHERE id = %s", (profissional_id,))
        dados = cursor.fetchone()
        conn.close()
        
        if dados:
            return Profissional(dados[1], dados[2], dados[3], dados[4], dados[0])
        return None
    
    def listar_profissionais(self, especialidade=None):
        """Lista profissionais, opcionalmente filtrando por especialidade."""
        conn = self._conectar()
        cursor = conn.cursor()
        
        if especialidade:
            cursor.execute("SELECT * FROM profissionais WHERE especialidade = %s ORDER BY nome", (especialidade,))
        else:
            cursor.execute("SELECT * FROM profissionais ORDER BY nome")
        
        dados = cursor.fetchall()
        conn.close()
        
        return [Profissional(d[1], d[2], d[3], d[4], d[0]) for d in dados]
    
    # ===== OPERAÇÕES COM CONSULTAS =====
    
    def adicionar_consulta(self, consulta):
        """Adiciona uma nova consulta ao banco de dados."""
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            cursor.execute(
                """
                    INSERT INTO consultas (id, paciente_id, profissional_id, data_hora, motivo, status, notas, data_criacao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    consulta.id,
                    consulta.paciente_id,
                    consulta.profissional_id,
                    consulta.data_hora,
                    consulta.motivo,
                    consulta.status.value,
                    consulta.notas,
                    consulta.data_criacao,
                ),
            )
            conn.commit()
            conn.close()
            return True
        except IntegrityError as e:
            print(f"Erro: {e}")
            return False
    
    def obter_consulta(self, consulta_id):
        """Obtém uma consulta pelo ID."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consultas WHERE id = %s", (consulta_id,))
        dados = cursor.fetchone()
        conn.close()
        
        if dados:
            consulta = Consulta(dados[1], dados[2], dados[3], dados[4], dados[5], dados[0])
            consulta.notas = dados[6]
            return consulta
        return None
    
    def listar_consultas(self, paciente_id=None, profissional_id=None, status=None):
        """Lista consultas com filtros opcionais."""
        conn = self._conectar()
        cursor = conn.cursor()
        
        query = "SELECT * FROM consultas WHERE 1=1"
        params = []
        
        if paciente_id:
            query += " AND paciente_id = %s"
            params.append(paciente_id)
        
        if profissional_id:
            query += " AND profissional_id = %s"
            params.append(profissional_id)
        
        if status:
            query += " AND status = %s"
            params.append(status)
        
        query += " ORDER BY data_hora"
        
        cursor.execute(query, tuple(params))
        dados = cursor.fetchall()
        conn.close()
        
        consultas = []
        for d in dados:
            consulta = Consulta(d[1], d[2], d[3], d[4], d[5], d[0])
            consulta.notas = d[6]
            consultas.append(consulta)
        
        return consultas
    
    def atualizar_status_consulta(self, consulta_id, novo_status):
        """Atualiza o status de uma consulta."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE consultas SET status = %s WHERE id = %s", (novo_status, consulta_id))
        conn.commit()
        conn.close()
    
    def atualizar_notas_consulta(self, consulta_id, notas):
        """Atualiza as notas de uma consulta."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE consultas SET notas = %s WHERE id = %s", (notas, consulta_id))
        conn.commit()
        conn.close()
    
    def deletar_consulta(self, consulta_id):
        """Deleta uma consulta do banco de dados."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultas WHERE id = %s", (consulta_id,))
        conn.commit()
        conn.close()
    
    def consultas_proximas(self, dias=7, data_inicio=None):
        """Retorna consultas agendadas para os próximos dias."""
        from datetime import datetime, timedelta
        if data_inicio is None:
            data_inicio = datetime.now()
        data_fim = data_inicio + timedelta(days=dias)
        
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT * FROM consultas 
                WHERE data_hora BETWEEN %s AND %s 
                AND status != 'cancelada'
                ORDER BY data_hora
            """,
            (data_inicio, data_fim),
        )
        
        dados = cursor.fetchall()
        conn.close()
        
        consultas = []
        for d in dados:
            consulta = Consulta(d[1], d[2], d[3], d[4], d[5], d[0])
            consulta.notas = d[6]
            consultas.append(consulta)
        
        return consultas

    # ===== OPERAÇÕES COM NOTIFICAÇÕES =====

    def adicionar_notificacao(self, notificacao):
        """Adiciona uma nova notificação ao banco de dados."""
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            cursor.execute(
                """
                    INSERT INTO notificacoes (id, consulta_id, tipo, ferramenta, agendamento, titulo, descricao, status, data_criacao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    notificacao.id,
                    notificacao.consulta_id,
                    notificacao.tipo,
                    notificacao.ferramenta,
                    notificacao.agendamento,
                    notificacao.titulo,
                    notificacao.descricao,
                    notificacao.status,
                    notificacao.data_criacao,
                ),
            )
            conn.commit()
            conn.close()
            return True
        except IntegrityError as e:
            print(f"Erro: {e}")
            return False

    def listar_notificacoes_por_consulta(self, consulta_id):
        """Lista todas as notificações de uma consulta."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notificacoes WHERE consulta_id = %s ORDER BY agendamento", (consulta_id,))
        dados = cursor.fetchall()
        conn.close()
        
        notificacoes = []
        for d in dados:
            notificacao = Notificacao(d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[0])
            notificacao.data_criacao = d[8]
            notificacoes.append(notificacao)
        
        return notificacoes

    def cancelar_notificacao(self, notificacao_id):
        """Cancela uma notificação se ela ainda estiver agendada."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE notificacoes SET status = 'cancelada' WHERE id = %s AND status = 'agendada'", (notificacao_id,))
        conn.commit()
        conn.close()
