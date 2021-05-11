from __future__ import annotations
from flask import request
from app import app, db
import logging
import models
import utils


@app.route("/", methods=["GET"])
@utils.as_json
def home() -> utils.JsonResponse:
  return {"message": "ok"}, 200


@app.route("/players/<username>", methods=["POST"])
@utils.as_json
def register_player(username: str) -> utils.JsonResponse:
  if player_exists(username):
    return {"error": "A player with that name already exists"}, 400

  new_player = models.PlayerRecord(username=username)
  db.session.add(new_player)
  db.session.commit()

  logging.info(f"Registered player with username '{username}'")

  return {}, 200

def player_exists(username: str) -> bool:
  return (models.PlayerRecord.query
    .filter(models.PlayerRecord.username == username)
    .count()) > 0

def game_exists(game_id: int) -> bool:
  return (models.GameRecord.query
    .filter(models.GameRecord.id == game_id)
    .count()) > 0

@app.route("/players/<username>", methods=["GET"])
@utils.as_json
def fetch_player(username: str) -> utils.JsonResponse:
  if player_exists(username):
    print("The username ", username, " is registered")
    return {"username": username}, 400
  else:
    print("This username is not registered", username)
    return {"error": "This username doesn't exist"}, 400

@app.route("/games", methods=["POST"])
@utils.as_json
def startGame() -> utils.JsonResponse:
  challenger = request.json.get("challenger")
  opponent = request.json.get("opponent")
  
  if not player_exists(challenger):
    return {"error": "The challenger is not registered"}, 404

  if not player_exists(opponent):
    return {"error": " The opponent doesn't exist"}, 404

  if challenger == "" or None : 
      return {"error": "Please enter a valid challenger name"}, 400
  
  if opponent == "" or None : 
      return {"error": "Please enter a valid opponent name"}, 400


  new_game = models.GameRecord(
    challenger_username = challenger,
    opponent_username = opponent,
    current_player = challenger,
    winner = None,
    can_move = True,
    board = "---------")
  db.session.add(new_game)
  db.session.commit()

  return {
    "game_id": new_game.id,
    "opponent_username": new_game.opponent_username,
    "challenger_username": new_game.challenger_username,
    "current_player": new_game.current_player,
    "winner": new_game.winner,
    "can_move": new_game.can_move,
    "board": new_game.board,
    "created_at": new_game.created_at
  }, 200

@app.route("/games/<game_id>", methods=["GET"])
@utils.as_json
def get_game(game_id:int) -> utils.JsonResponse:

  if game_exists(game_id):
    game = models.GameRecord.query.filter(models.GameRecord.id == game_id).first()
      
    return{
      "game_id": game.id,
      "opponent_username": game.opponent_username,
      "challenger_username": game.challenger_username,
      "current_player": game.current_player,
      "winner": game.winner,
      "can_move": game.can_move,
      "board": game.board,
      "created_at": game.created_at
    }, 200

  else:
    return {"error": "This game does not !!!!!!!"}, 404

@app.route("/games/<game_id>/moves", methods=["POST"])
@utils.as_json
def playGame(game_id: int) -> utils.JsonResponse:
  col = request.json.get("col")
  row = request.json.get("row")
  username = request.json.get("username")
 
  game = models.GameRecord.query.filter(models.GameRecord.id == game_id).first()
  print(game.challenger_username)
  print(username)

  if not game_exists(game_id):
    return {"error": "This game does not exist"}, 404

  if col == None or col == "" : 
    return {"error": "Can't find column number"}, 400
  
  if row == None or row == "" : 
    return {"error": "Can't find row number"}, 400
  
  if not player_exists(username):
    return {"error": "The player does not exist"}, 400 
    
  try: 
    row = int(row)
  except:
    return{"error": "The row number is not an integer, please provide an integer"}, 400

  try:
    col = int(col)
  except:
    return{"error": "The col number is s not an integer, please provide an integer"}, 400

  if row > 2 or row < 0:
    return {"error": "The row number is currently out of bounds"}, 400

  if col > 2 or col < 0:
    return {"error": "The col number is currently out of bounds"}, 400

 
 

  position = 0

  if row == 0 and col == 0:
    position = 0

  elif row == 0 and col == 1:
    position = 1
  
  elif row == 0 and col == 2:
    position = 2

  elif row == 1 and col == 0:
    position = 3

  elif row == 1 and col == 1:
    position = 4

  elif row == 1 and col == 2:
    position = 5

  elif row == 2 and col == 0:
    position = 6

  elif row == 2 and col == 1:
    position = 7

  else:
    position = 8  
  

  if username == game.challenger_username:
    print(game.challenger_username)
    
    if game.board[position] == "-":
      game.board = game.board[:position] + "x" + game.board[position + 1:]
    else:
      return {"error": "The position has already been marked"}, 400
    game.current_player = game.opponent_username

    if game.board[0] == "x" and game.board[1] == "x" and game.board[2] == "x":
      game.winner = game.challenger_username
      game.can_move = False

    elif game.board[3] == "x" and game.board[4] == "x" and game.board[5] == "x":
      game.winner = game.challenger_username
      game.can_move = False

    elif game.board[6] == "x" and game.board[7] == "x" and game.board[8] == "x":
      game.winner = game.challenger_username
      game.can_move = False
    
    elif game.board[0] == "x" and game.board[3] == "x" and game.board[6] == "x":
      game.winner = game.challenger_username
      game.can_move = False
    
    elif game.board[1] == "x" and game.board[4] == "x" and game.board[7] == "x":
      game.winner = game.challenger_username
      game.can_move = False

    elif game.board[2] == "x" and game.board[5] == "x" and game.board[8] == "x":
      game.winner = game.challenger_username
      game.can_move = False

    elif game.board[0] == "x" and game.board[4] == "x" and game.board[8] == "x":
      game.winner = game.challenger_username
      game.can_move = False

    elif game.board[2] == "x" and game.board[4] == "x" and game.board[6] == "x":
      game.winner = game.challenger_username
      game.can_move = False


  elif username == game.opponent_username:
    if game.board[position] == "-":
      game.board = game.board[:position] + "o" + game.board[position + 1:]
    else:
      return {"error": "The position has already been marked"}, 400
    game.current_player = game.challenger_username
    
    if game.board[0] == "o" and game.board[1] == "o" and game.board[2] == "o":
      game.winner = game.opponent_username
      game.can_move = False

    elif game.board[3] == "o" and game.board[4] == "o" and game.board[5] == "o":
      game.winner = game.opponent_username
      game.can_move = False

    elif game.board[6] == "o" and game.board[7] == "o" and game.board[8] == "o":
      game.winner = game.opponent_username
      game.can_move = False
    
    elif game.board[0] == "o" and game.board[3] == "o" and game.board[6] == "o":
      game.winner = game.opponent_username
      game.can_move = False
    
    elif game.board[1] == "o" and game.board[4] == "o" and game.board[7] == "o":
      game.winner = game.opponent_username
      game.can_move = False

    elif game.board[2] == "o" and game.board[5] == "o" and game.board[8] == "o":
      game.winner = game.opponent_username
      game.can_move = False

    elif game.board[0] == "o" and game.board[4] == "o" and game.board[8] == "o":
      game.winner = game.opponent_username
      game.can_move = False

    elif game.board[2] == "o" and game.board[4] == "o" and game.board[6] == "o":
      game.winner = game.opponent_username
      game.can_move = False
      
  db.session.commit()

  return{
    "game_id": game.id,
    "opponent_username": game.opponent_username,
    "challenger_username": game.challenger_username,
    "current_player": game.current_player,
    "winner": game.winner,
    "can_move": game.can_move,
    "board": game.board,
    "created_at": game.created_at
  }, 200
    

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)


