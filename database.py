"""Gerenciamento de banco de dados SQLite para o agendador."""
import sqlite3
import os
from datetime import datetime
from models import Paciente, Profissional, Consulta, StatusConsulta


class Database:
    """Gerencia a conexão e operações com o banco de dados SQLite."""
    
    def __init__(self, db_path="agendador.db"):
        self.db_path = db_path
        self.criar_tabelas()
    
    def _conectar(self):
        """Cria uma conexão com o banco de dados."""
        return sqlite3.connect(self.db_path)
    
    def criar_tabelas(self):
        """Cria as tabelas do banco de dados se não existirem."""
        conn = self._conectar()
        cursor = conn.cursor()
        
        # Tabela de pacientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT,
                data_criacao TIMESTAMP
            )
        """)
        
        # Tabela de profissionais
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
        
        # Tabela de consultas
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
        
        conn.commit()
        conn.close()
    
    # ===== OPERAÇÕES COM PACIENTES =====
    
    def adicionar_paciente(self, paciente):
        """Adiciona um novo paciente ao banco de dados."""
        try:
            conn = self._conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pacientes (id, nome, cpf, telefone, email, data_criacao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (paciente.id, paciente.nome, paciente.cpf, paciente.telefone, paciente.email, paciente.data_criacao))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Erro: {e}")
            return False
    
    def obter_paciente(self, paciente_id):
        """Obtém um paciente pelo ID."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,))
        dados = cursor.fetchone()
        conn.close()
        
        if dados:
            return Paciente(dados[1], dados[2], dados[3], dados[4], dados[0])
        return None
    
    def obter_paciente_cpf(self, cpf):
        """Obtém um paciente pelo CPF."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE cpf = ?", (cpf,))
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
            cursor.execute("""
                INSERT INTO profissionais (id, nome, especialidade, crm, telefone, data_criacao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (profissional.id, profissional.nome, profissional.especialidade, profissional.crm, profissional.telefone, profissional.data_criacao))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Erro: {e}")
            return False
    
    def obter_profissional(self, profissional_id):
        """Obtém um profissional pelo ID."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM profissionais WHERE id = ?", (profissional_id,))
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
            cursor.execute("SELECT * FROM profissionais WHERE especialidade = ? ORDER BY nome", (especialidade,))
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
            cursor.execute("""
                INSERT INTO consultas (id, paciente_id, profissional_id, data_hora, motivo, status, notas, data_criacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (consulta.id, consulta.paciente_id, consulta.profissional_id, consulta.data_hora, 
                  consulta.motivo, consulta.status.value, consulta.notas, consulta.data_criacao))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Erro: {e}")
            return False
    
    def obter_consulta(self, consulta_id):
        """Obtém uma consulta pelo ID."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consultas WHERE id = ?", (consulta_id,))
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
            query += " AND paciente_id = ?"
            params.append(paciente_id)
        
        if profissional_id:
            query += " AND profissional_id = ?"
            params.append(profissional_id)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY data_hora"
        
        cursor.execute(query, params)
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
        cursor.execute("UPDATE consultas SET status = ? WHERE id = ?", (novo_status, consulta_id))
        conn.commit()
        conn.close()
    
    def atualizar_notas_consulta(self, consulta_id, notas):
        """Atualiza as notas de uma consulta."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE consultas SET notas = ? WHERE id = ?", (notas, consulta_id))
        conn.commit()
        conn.close()
    
    def deletar_consulta(self, consulta_id):
        """Deleta uma consulta do banco de dados."""
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consultas WHERE id = ?", (consulta_id,))
        conn.commit()
        conn.close()
    
    def consultas_proximas(self, dias=7):
        """Retorna consultas agendadas para os próximos dias."""
        from datetime import datetime, timedelta
        data_inicio = datetime.now()
        data_fim = data_inicio + timedelta(days=dias)
        
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM consultas 
            WHERE data_hora BETWEEN ? AND ? 
            AND status != 'cancelada'
            ORDER BY data_hora
        """, (data_inicio, data_fim))
        
        dados = cursor.fetchall()
        conn.close()
        
        consultas = []
        for d in dados:
            consulta = Consulta(d[1], d[2], d[3], d[4], d[5], d[0])
            consulta.notas = d[6]
            consultas.append(consulta)
        
        return consultas
