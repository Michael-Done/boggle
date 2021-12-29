from flask import Flask, render_template, url_for, request, redirect, jsonify, session, Response
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask.wrappers import Response
from app import *

server_app = Flask(__name__)
server_app.secret_key = "snmdlepijsnechs"

server_socket = SocketIO(server_app)

coordinator = GameCoordinator()
PNAME_KEY = 'player_name'
GAMEID_KEY = 'game_id'

## HTTP server handlers
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

   if PNAME_KEY not in session:
      return redirect('/' + str(game_id) + '/new_player')
   if GAMEID_KEY not in session and session[GAMEID_KEY] != game_id:
      return redirect('/' + str(game_id) + '/new_player')

   player = session[PNAME_KEY]
   game_instance = coordinator.game_list[game_id]

   if player not in game_instance.player_list:
      game_instance.add_player(player)
      session[PNAME_KEY] = player
      session[GAMEID_KEY] = game_id

   game_instance.touch()
   players = list(game_instance.player_list.keys())
   return render_template('game.html', game_id=game_id, player=player, players=players)


@server_app.route('/<game_id>/new_player', methods=['GET','POST'])
def game_new_player(game_id):
   if game_id not in coordinator.game_list:
      return redirect('/')

   game_instance = coordinator.game_list[game_id]

   if request.method == 'GET':
      game_instance.touch()
      return render_template('new_player.html', msg='')

   if request.method == 'POST':
      if 'player_name' not in request.form:
         return "\"player_name\" must be submitted to create a new player", 500

      player = request.form['player_name']

      if player in game_instance.player_list:
         return render_template('new_player.html', msg=(str(player) + ' is already in this game'))

      game_instance.touch()
      p = game_instance.add_player(player)
      session[PNAME_KEY] = p.name
      session[GAMEID_KEY] = game_id
      return redirect('/' + str(game_id))

## Socket game event handlers
@server_socket.on('connect')
def on_connect(param):
   game_id = session[GAMEID_KEY]
   player = session[PNAME_KEY]

   if game_id not in coordinator.game_list:
      print('Error, game', game_id, 'does not exits')
      send('Error, game ' + game_id + ' does not exits')
      return
   
   game_instance = coordinator.game_list[game_id]
   game_instance.touch()

   if player not in game_instance.player_list:
      print('Error, player', player, 'is not in game', game_id)
      send('Error, player ' + player + ' is not in game ' + game_id)
      return

   join_room(game_id)
   server_socket.emit('player_list', list(game_instance.player_list.keys()), to=game_id)
   print('Player', player, 'connected to', game_id)

@server_socket.on('disconnect')
def on_disconnect():
   game_id = session[GAMEID_KEY]
   player = session[PNAME_KEY]

   if game_id not in coordinator.game_list:
      print('Error, game', game_id, 'does not exits')
      send('Error, game ' + game_id + ' does not exits')
      return
   
   game_instance = coordinator.game_list[game_id]

   if player not in game_instance.player_list:
      print('Error, player', player, 'is not in game', game_id)
      send('Error, player ' + player + ' is not in game ' + game_id)
      return

   game_instance.player_list.pop(player)
   leave_room(game_id)
   server_socket.emit('player_list', list(game_instance.player_list.keys()), to=game_id)
   print("Player", player, "disconnected from", game_id)

@server_socket.on('start_game')
def start_game(game_settings):
   player = session[PNAME_KEY]
   game_id = session[GAMEID_KEY]

   if game_id not in coordinator.game_list:
      print('Error, game', game_id, 'does not exits')
      send('Error, game ' + game_id + ' does not exits')
      return

   game_instance = coordinator.game_list[game_id]
   game_instance.new_round()
   server_socket.emit('game_board', game_instance.board, to=game_id)


if __name__ == '__main__':
   server_socket.run(server_app, debug=True)