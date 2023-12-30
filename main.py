import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from scr.routes import notes, users, tags, auth
from scr.conf.config import config

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix="/api")
app.include_router(tags.router, prefix='/api')
app.include_router(notes.router, prefix='/api')

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/")
def read_root():
    return {"message": "Hello World GoIT Expanded Web developer"}
