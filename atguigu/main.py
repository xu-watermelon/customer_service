from uvicorn import run
from atguigu.api import app          
from atguigu.config.config import settings
from atguigu.utils.database import init_db_engine  
if __name__ == "__main__":
    init_db_engine()
    run("atguigu.api.app:app", host=settings.app_host, port=settings.app_port)
