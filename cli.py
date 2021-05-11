from __future__ import annotations

import client
import models

t3 = client.Client("http://isaac-t3.csci390.com:5000")

def get_menu_choice() -> int:
  while True:
    print("Please choose a menu option.")
    print("1. Register a player")
    print("2. Play a new game")
    print("3. Resume existing game")
    print("4. Quit")

    menu_str = input("Where do you want to go today? ")

    if menu_str.isnumeric():
      menu_int = int(menu_str)

      if menu_int >= 1 and menu_int <= 4:
        return menu_int

    print("Um, no")

def register_player() -> None:
  while True:
    username = input("Enter player's username: ")

    if username.strip():
      break
    else:
      print("Username cannot be blank")

  try:
    t3.register_player(username)
  except client.ClientError as e:
    print(f"Error: {e.args[0]}")

def play_game(game_id: int = None) -> None:
  if game_id:
    game = t3.get_game(game_id).body
  else:
    challenger_username = input("Enter challenger username: ")
    opponent_username = input("Enter opponent's username: ")

    game = t3.create_game(challenger_username, opponent_username).body
    print(f"Started game between {challenger_username} and {opponent_username} with id {game['game_id']}")

  while not game["winner"] and game["can_move"]:
    current_player = game["current_player"]
    board = models.Board.from_str(game["board"])
    print(repr(board))

    while True:
      move_str = input(f"Your move, {current_player} (row, col): ")
      row_str, col_str = move_str.split(",")
      row = int(row_str.strip())
      col = int(col_str.strip())

      try:
        move = t3.move(game["game_id"], current_player, row, col).body
        game = move
        break
      except client.ClientError as e:
        print(f"Error: {e.args[0]}")

  board = models.Board.from_str(game["board"])
  print(repr(board))

  print(f"Congratulations {game['winner']}, you won!")

def resume_game() -> None:
  while True:
    game_id_str = input("Enter game ID: ")

    if game_id_str.isnumeric():
      game_id = int(game_id_str)
      break
    else:
      print("Game ID must be a number")

  play_game(game_id)

if __name__ == "__main__":
  print("Welcome to tic-tac-toe!")

  while True:
    op = get_menu_choice()

    if op == 1:
      register_player()
    elif op == 2:
      play_game()
    elif op == 3:
      resume_game()
    else:
      break
