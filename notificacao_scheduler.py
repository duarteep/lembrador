"""Scheduler de notificações para o agendador de consultas.

Este script roda continuamente verificando notificações pendentes a cada 15 minutos.
Quando encontra notificações agendadas para o momento atual ou passado (nos últimos 30 minutos),
envia uma mensagem detalhada via WhatsApp para o paciente contendo:
- Data e horário da consulta
- Status atual da consulta
- Nome e especialidade do profissional
- Motivo da consulta
- Título e descrição da notificação

Notificações vencidas há mais de 30 minutos são automaticamente marcadas como falha.
"""

import time
from datetime import datetime, timedelta
from utils_whatsapp import enviar_mensagem
from database import Database
from config import BASE_URL


class NotificacaoScheduler:
    """Gerencia o agendamento e envio de notificações."""

    def __init__(self):
        self.intervalo_minutos = 15
        self.db = Database()  # Reutiliza a classe Database existente
        self.limite_minutos = 30  # Notificações vencidas há mais de 30 minutos são marcadas como falha

    def marcar_notificacoes_antigas_como_falha(self):
        """Marca notificações agendadas vencidas há mais de 30 minutos como falha."""
        conn = self.db._conectar()
        cursor = conn.cursor()

        limite_tempo = datetime.now() - timedelta(minutes=self.limite_minutos)
        cursor.execute(
            "UPDATE notificacoes SET status = 'falha' WHERE status = 'agendada' AND agendamento < %s",
            (limite_tempo,)
        )
        notificacoes_marcadas = cursor.rowcount
        conn.commit()
        conn.close()

        if notificacoes_marcadas > 0:
            print(f"Marcadas {notificacoes_marcadas} notificações antigas como falha.")

    def buscar_notificacoes_pendentes(self):
        """Busca notificações agendadas para envio (status='agendada', agendamento <= agora, mas não mais antigas que 30 minutos)."""
        conn = self.db._conectar()
        cursor = conn.cursor()

        agora = datetime.now()
        limite_tempo = agora - timedelta(minutes=self.limite_minutos)
        cursor.execute("""
            SELECT n.id, n.consulta_id, n.titulo, n.descricao, n.ferramenta,
                   p.telefone, p.nome, c.data_hora, c.status, c.motivo,
                   pr.nome, pr.especialidade
            FROM notificacoes n
            JOIN consultas c ON n.consulta_id = c.id
            JOIN pacientes p ON c.paciente_id = p.id
            JOIN profissionais pr ON c.profissional_id = pr.id
            WHERE n.status = 'agendada'
            AND n.agendamento <= %s
            AND n.agendamento >= %s
            AND n.ferramenta = 'whatsapp'
            ORDER BY n.agendamento
        """, (agora, limite_tempo))

        notificacoes = cursor.fetchall()
        conn.close()

        return notificacoes

    def atualizar_status_notificacao(self, notificacao_id, novo_status):
        """Atualiza o status de uma notificação."""
        conn = self.db._conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE notificacoes SET status = %s WHERE id = %s",
            (novo_status, notificacao_id)
        )
        conn.commit()
        conn.close()

    def enviar_notificacao_whatsapp(self, notificacao):
        """Envia notificação via WhatsApp."""
        notificacao_id, consulta_id, titulo, descricao, ferramenta, telefone, nome_paciente, data_hora_consulta, status_consulta, motivo_consulta, nome_profissional, especialidade_profissional = notificacao

        # Formatar data e hora da consulta
        data_formatada = data_hora_consulta.strftime("%d/%m/%Y")
        hora_formatada = data_hora_consulta.strftime("%H:%M")

        # Mapear status para português
        status_map = {
            'agendada': 'Agendada',
            'confirmada': 'Confirmada',
            'realizada': 'Realizada',
            'cancelada': 'Cancelada'
        }
        status_formatado = status_map.get(status_consulta, status_consulta.title())

        # Formatar mensagem base
        mensagem = f"""Olá {nome_paciente}! 👋

🚨 *LEMBRETE DE CONSULTA*

📅 *Data:* {data_formatada}
🕐 *Horário:* {hora_formatada}
👨‍⚕️ *Profissional:* {nome_profissional}
🏥 *Especialidade:* {especialidade_profissional}
📋 *Status:* {status_formatado}
📝 *Motivo:* {motivo_consulta}

"""

        if status_consulta != 'confirmada':
            link_confirmacao = f"{BASE_URL}/consultas/{consulta_id}/confirmacao"
            mensagem += f"Por favor, confirme ou cancele sua consulta aqui:\n{link_confirmacao}\n\n"

        mensagem += "Por favor, confirme sua presença ou entre em contato se precisar reagendar."
        try:
            # Enviar mensagem
            enviar_mensagem(telefone, mensagem)
            print(f"✅ Notificação enviada com sucesso via WhatsApp para {nome_paciente} (+55{telefone})")
            self.atualizar_status_notificacao(notificacao_id, 'enviada')
            return True
        except Exception as e:
            print(f"❌ Falha ao enviar notificação para {nome_paciente}: {e}")
            self.atualizar_status_notificacao(notificacao_id, 'falha')
            return False

    def processar_notificacoes(self):
        """Processa todas as notificações pendentes."""
        # Primeiro, marca notificações muito antigas como falha
        self.marcar_notificacoes_antigas_como_falha()

        # Depois, busca notificações recentes para envio
        notificacoes = self.buscar_notificacoes_pendentes()

        if not notificacoes:
            print("Nenhuma notificação pendente encontrada.")
            return

        print(f"Encontradas {len(notificacoes)} notificações pendentes para envio.")

        for notificacao in notificacoes:
            self.enviar_notificacao_whatsapp(notificacao)

    def executar(self):
        """Executa o scheduler em loop infinito."""
        print("Iniciando scheduler de notificações...")
        print(f"Verificando a cada {self.intervalo_minutos} minutos.")

        while True:
            try:
                print(f"\n[{datetime.now()}] Verificando notificações...")
                self.processar_notificacoes()
                print(f"Aguardando {self.intervalo_minutos} minutos...")
                time.sleep(self.intervalo_minutos * 60)
            except KeyboardInterrupt:
                print("\nScheduler interrompido pelo usuário.")
                break
            except Exception as e:
                print(f"Erro no scheduler: {e}")
                print("Tentando novamente em 1 minuto...")
                time.sleep(60)


if __name__ == "__main__":
    scheduler = NotificacaoScheduler()
    scheduler.executar()