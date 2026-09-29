from flask import Flask, request, jsonify

app = Flask(__name__)

CHAVES_VALIDAS = {
    "MINHA-KEY-VIP-01": "Ativo",
    "TESTE-123": "Ativo",
    "HAROXIT123": "Ativo"
    "USER-PREMIUM-99": "Ativo"
}

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json
    user_key = data.get("key")
    protocol = data.get("protocol")
    device_id = data.get("device_id") # O app envia isso, vamos capturar

    if protocol == "GR-AUTH-V1" and user_key in CHAVES_VALIDAS:
        # Aqui simulamos a resposta de um painel profissional
        return jsonify({
            "status": 1, 
            "message": "Welcome to Premium!",
            "build_id": "1.0.0",           # Simula a versão correta
            "integrity_version": "1",     # Simula integridade do app
            "session_id": f"SESS_{device_id}", # Cria uma sessão falsa usando o ID do aparelho
            "is_banned": 0,
            "show_key": 0,
            "expiry": "2026-12-31"
        }), 200
    else:
        return jsonify({"status": 0, "message": "Invalid Key!"}), 401

@app.route('/')
def home():
    return "EmpireExits Clone Server Online! 🚀"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
