import logging
import uvicorn
from settings.settings import config
from fastapi import FastAPI
from routes.routes import routes

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    format='%(asctime)s - %(message)s | %(levelname)s ',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO
)

app = FastAPI()

app.include_router(routes)

if __name__ == "__main__":
    logging.info(f'Start server {config.server_config.port}')
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=config.server_config.port,
                log_level=config.server_config.log_level)