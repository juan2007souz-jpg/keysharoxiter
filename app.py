from flask import Flask, request, Response

app = Flask(__name__)

# Suas keys de venda
CHAVES_VALIDAS = {
    "MINHA-KEY-VIP-01": "Ativo",
    "TESTE-123": "Ativo",
    "HAROXIT123": "Ativo",
    "USER-PREMIUM-99": "Ativo"
}

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json
    user_key = data.get("key")
    protocol = data.get("protocol")
    device_id = data.get("device_id", "unknown")

    # Verificação de protocolo e chave
    if protocol == "GR-AUTH-V1" and user_key in CHAVES_VALIDAS:
        # IMPORTANTE: O Mod Menu espera este formato de texto, não um JSON comum.
        # Note que status=1 e is_banned=0 são os gatilhos para abrir o menu.
        response_text = (
            f"GR-AUTH-V1\n"
            f"status=1\n"
            f"message_b64=V2VsY29tZSB0byBWRVAgT3BlbCB8IFlvdSBBcmUgT24h\n" # "Welcome to VIP Open | You Are On!" em Base64
            f"device_id={device_id}\n"
            f"is_banned=0\n"
            f"showPannel=1\n"
            f"session_id=SESS_{device_id}\n"
            f"expires_at=20261231"
        )
        
        # Retornamos como 'text/plain' para o app não se confundir com JSON
        return Response(response_text, mimetype='text/plain'), 200
    else:
        # Resposta de erro no formato do protocolo
        error_text = "GR-AUTH-V1\nstatus=0\nmessage_b64=S2V5IEludmFsaWQh" # "Key Invalid!" em Base64
        return Response(error_text, mimetype='text/plain'), 401

@app.route('/')
def home():
    return "Servidor de Autenticação VIP Online! 🚀"

if __name__ == '__main__':
    # Lembre-se de abrir a porta 5000 no seu firewall/ VPS
    app.run(host='0.0.0.0', port=5000)
