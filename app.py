from flask import Flask, request, Response
import base64

app = Flask(__name__)

# --- BANCO DE DADOS DE KEYS (Onde você controla quem entra) ---
# Formato: "KEY": "STATUS"
CHAVES_VIP = {
    "VIP-2026-SENSACIONAL": "Ativo",
    "HAROXIT-PREMIUM": "Ativo",
    "TESTE-GRATIS-01": "Ativo"
}

@app.route('/auth', methods=['POST', 'GET'])
def authenticate():
    # Captura a key enviada pelo mod menu
    # O menu pode enviar via JSON (POST) ou via URL (GET)
    user_key = request.args.get('key') or (request.json.get('key') if request.is_json else None)
    device_id = request.args.get('device_id') or (request.json.get('device_id') if request.is_json else "unknown_device")
    
    # 1. Verificamos se a key está na nossa lista VIP
    if user_key in CHAVES_VIP:
        # MENSAGEM DE BOAS-VINDAS (Em Base64 para o app não crashar)
        # Texto: "Acesso Concedido! Bem-vindo ao Menu VIP do [Seu Nome]"
        welcome_msg = base64.b64encode(b"Acesso Concedido! Bem-vindo ao Menu VIP").decode('utf-8')
        
        # ESTA É A RESPOSTA MÁGICA QUE O .DYLIB ESPERA
        # status=1 -> Abre o Menu
        # is_banned=0 -> Não está banido
        # showPannel=1 -> Mostra o painel de cheats
        response_body = (
            f"GR-AUTH-V1\n"
            f"status=1\n"
            f"message_b64={welcome_msg}\n"
            f"device_id={device_id}\n"
            f"is_banned=0\n"
            f"showPannel=1\n"
            f"session_id=SESS_{device_id}\n"
            f"expires_at=20300101" # Validade longa para o cliente não reclamar
        )
        return Response(response_body, mimetype='text/plain'), 200
    
    else:
        # RESPOSTA DE ERRO
        # status=0 -> Key Inválida ou Expirada
        error_msg = base64.b64encode(b"Chave Invalida ou Expirada!").decode('utf-8')
        response_body = f"GR-AUTH-V1\nstatus=0\nmessage_b64={error_msg}"
        return Response(response_body, mimetype='text/plain'), 401

@app.route('/')
def home():
    return "Servidor GR-AUTH V1 Online - Gestao de Licencas VIP 🚀"

if __name__ == '__main__':
    # Porta 80 é a padrão para sites (HTTP), use-a se estiver em VPS
    app.run(host='0.0.0.0', port=80)
