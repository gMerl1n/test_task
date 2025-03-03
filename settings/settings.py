import os
import json
from pydantic import BaseModel
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL: str = f"sqlite+aiosqlite:///task_db.sqlite3"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
session_local = sessionmaker(autoflush=False, bind=engine, class_=AsyncSession)

config_path = os.path.join(BASE_DIR, 'settings', "config.json")

with open(config_path) as file:
    config = json.load(file)
    server_config = config["server"]


class ServerConfig(BaseModel):
    port: int
    log_level: str


class Settings:
    server_config = ServerConfig(port=server_config["port"], log_level=server_config["log_level"])


config = Settings()
