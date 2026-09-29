from flask import Flask, request, jsonify

app = Flask(__name__)

# Aqui é onde você coloca as suas chaves. 
# Você pode adicionar quantas quiser.
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

    # Verifica se o protocolo é o correto e se a chave existe na lista
    if protocol == "GR-AUTH-V1" and user_key in CHAVES_VALIDAS:
        return jsonify({
            "status": "SUCCESS", 
            "message": "Welcome to Empire Exits Premium!",
            "expiry": "2026-12-31" 
        }), 200
    else:
        return jsonify({
            "status": "INVALID", 
            "message": "Chave inválida ou expirada!"
        }), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
