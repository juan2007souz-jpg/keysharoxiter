from flask import Flask, request, jsonify

app = Flask(__name__)

# Suas chaves continuam as mesmas
CHAVES_VALIDAS = {
    "MINHA-KEY-VIP-01": "Ativo",
    "TESTE-123": "Ativo",
    "USER-PREMIUM-99": "Ativo"
}

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json
    user_key = data.get("key")
    protocol = data.get("protocol")

    if protocol == "GR-AUTH-V1" and user_key in CHAVES_VALIDAS:
        return jsonify({
            "status": 1,                   # Mudamos para 1 (número), que é o padrão de 'True'
            "message": "Success",         # Mensagem simples
            "build_id": "1.0.0",          # Enganando a versão do build
            "integrity_version": "1",     # Enganando a versão de integridade
            "session_id": "VALID_SESSION", # Simulando uma sessão ativa
            "expiry": "2026-12-31" 
        }), 200
    else:
        return jsonify({
            "status": 0,                   # 0 para 'False'
            "message": "Chave invalida!"
        }), 401

@app.route('/')
def home():
    return "Servidor de Keys Online e Atualizado! 🚀"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
