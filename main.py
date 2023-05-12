from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi_limiter.depends import FastAPILimiter
import redis.asyncio as redis
from sqlalchemy import text
from sqlalchemy.orm import Session
import uvicorn


from src.conf.config import settings
from src.conf.messages import *
from src.database.db import get_db
# from src.routes import pictures
from src.routes import auth


app = FastAPI()
app.include_router(auth.router, prefix='/api')
# app.include_router(pictures.router, prefix='/api')


@app.on_event('startup')
async def startup():
    redis_client = redis.Redis(
                               host=settings.redis_host, 
                               port=settings.redis_port, 
                               db=0, 
                               password=settings.redis_password
                               )
    await FastAPILimiter.init(redis_client)


@app.get('/api/healthchecker')
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text('SELECT 1')).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail=MSC500_DATABASE_CONFIG)
        
        return {'message': WELCOME_FASTAPI}
    
    except Exception as e:
        print(e)  # To log TODO
        raise HTTPException(status_code=500, detail=MSC500_DATABASE_CONNECT)


@app.get('/')
def read_root():
    return {'message': WELCOME}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


# alembic init migrations
# alembic revision --autogenerate -m 'Init'
# alembic upgrade head
