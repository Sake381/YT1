from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # dozvoljava zahteve sa frontend sa drugog origin-a

# Memorija poruka
messages = []  # svaka poruka je dict: {id, text, sender: 'user'|'agent'}

SUPPORT_CODE = "12345"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    code = data.get('code')
    if code == SUPPORT_CODE:
        return jsonify({"success": True, "role": "agent"})
    else:
        return jsonify({"success": False})

@app.route('/messages', methods=['GET', 'POST'])
def messages_handler():
    if request.method == 'GET':
        # vrati sve poruke
        return jsonify(messages)
    elif request.method == 'POST':
        data = request.json
        text = data.get('text', '').strip()
        sender = data.get('sender', 'user')  # user ili agent
        if not text:
            return jsonify({"success": False, "error": "Empty message"}), 400
        # Dodaj id
        msg_id = len(messages) + 1
        messages.append({"id": msg_id, "text": text, "sender": sender})
        return jsonify({"success": True, "message": messages[-1]})

if __name__ == '__main__':
    app.run(debug=True)
