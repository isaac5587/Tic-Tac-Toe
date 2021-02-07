from __future__ import annotations

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

  if username == "cerebro":
    return {"error": "Cannot register a player with the special username 'cerebro'"}, 400

  new_player = models.PlayerRecord(username=username)
  db.session.add(new_player)
  db.session.commit()

  logging.info(f"Registered player with username '{username}'")

  return {}, 200


def player_exists(username: str) -> bool:
  return (models.PlayerRecord.query
    .filter(models.PlayerRecord.username == username)
    .count()) > 0


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
