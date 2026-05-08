import pywhatkit as kit

def enviar_mensagem(numero_telefone, mensagem):
    # Envia a mensagem imediatamente (ele abrirá o WhatsApp Web no navegador padrão)
    # O parâmetro '15' é o tempo de espera para o navegador carregar antes de enviar
    try:
        kit.sendwhatmsg_instantly("+55" + numero_telefone, mensagem, wait_time=15, tab_close=True)
        #print("Mensagem enviada com sucesso para o WhatsApp " + numero_telefone)
    except Exception as e: 
        print(f"Falha ao enviar mensagem para o WhatsApp: {e}")