from __future__ import annotations
from typing import Type

from app import db
from datetime import datetime


def timestamps(klass: Type[db.Model]) -> None:
  klass.created_at = db.Column(
    db.DateTime, nullable=False, default=datetime.now)
  klass.updated_at = db.Column(
    db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class PlayerRecord(db.Model):
  __tablename__ = "players"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(255), nullable=False)


timestamps(PlayerRecord)
