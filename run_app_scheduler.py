"""Executa o Flask e o scheduler de notificações em paralelo."""

import threading
from index import app
from notificacao_scheduler import NotificacaoScheduler


def iniciar_scheduler():
    scheduler = NotificacaoScheduler()
    scheduler.executar()


if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=iniciar_scheduler, daemon=True)
    scheduler_thread.start()

    # Use use_reloader=False para evitar que o Flask reinicie o processo e duplique o thread.
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
