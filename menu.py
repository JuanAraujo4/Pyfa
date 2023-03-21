from base import base
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Bem vindo a API do Pyfa!"

@app.route("/joga/<entity>/<player>")
def checa_se_jogador_esta_no_time_ou_selecao(entity, player):
    check = base.check_player_in_entity(entity, player)
    return jsonify(check)

app.run(debug=True)
