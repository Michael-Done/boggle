from flask import Flask, render_template, url_for, request, redirect, jsonify, session, Response
from flask.wrappers import Response
from app import *

server_app = Flask(__name__)
server_app.secret_key = "snmdlepijsnechs"

coordinator = GameCoordinator()
PNAME_KEY = 'player_name'

@server_app.route('/', methods=['GET'])
def root_home():
   coordinator.flush_inactive_games()
   return render_template('home.html')

@server_app.route('/', methods=['POST'])
def root_new():
   coordinator.flush_inactive_games()
   game_id = coordinator.new_game()
   return redirect('/' + str(game_id))

@server_app.route('/<game_id>', methods=['GET'])
def game_view(game_id):
   if game_id not in coordinator.game_list:
      return redirect('/')
   elif PNAME_KEY in session:
      if session[PNAME_KEY] in coordinator.game_list[game_id].player_list:
         players = coordinator.game_list[game_id].player_list.keys()
         return render_template('game.html', game_id=game_id, player=session[PNAME_KEY], players=players)
      else:
         session.pop(PNAME_KEY)
         coordinator.game_list[game_id].touch()
         return render_template('new_player.html')
   else:
      coordinator.game_list[game_id].touch()
      return render_template('new_player.html')

@server_app.route('/<game_id>', methods=['POST'])
def game_new_player(game_id):
   if 'player_name' in request.form and game_id in coordinator.game_list:
      p = coordinator.game_list[game_id].add_player(request.form['player_name'])
      if p == None:
         return "Player already exists"
      else:
         session[PNAME_KEY] = p.name
         return redirect('/' + str(game_id))
   else:
      return redirect('/' + str(game_id))

@server_app.route('/<game_id>/start_game', methods=['POST'])
def game_start(game_id):
   if game_id in coordinator.game_list:
      game_instance = coordinator.game_list[game_id]
      if 'round_timer' in request.form:
         game_instance.round_timer = int(request.form['round_timer'])
      game_instance.new_round()
      return jsonify({'board': game_instance.board}), 200
   return Response(), 200


@server_app.route('/status', methods=['POST'])
def status_receive():
   # TODO change the game status to web socket
   data = request.get_json()
   if 'game_id' in data and data['game_id'] in coordinator.game_list:
      game_instance = coordinator.game_list[data['game_id']]
      game_instance.touch()
      if 'player_name' in data and data['player_name'] in game_instance.player_list:
         game_instance.player_list[data['player_name']].touch()
         return jsonify(game_instance.get_state()), 200
   return Response(), 200

if __name__ == '__main__':
   server_app.run(debug=True)