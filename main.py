import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from scr.routes import notes, users, tags, auth, cloud
from scr.conf.config import config
from fastapi.responses import HTMLResponse

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
app.include_router(cloud.router, prefix='/api')

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, encoding="utf-8",
                          password=config.REDIS_PASSWORD, decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <body>
            <h1>Hello world, Team09 Python16 GoIT present Coursework on FastAPI</h1>
            <a href="/docs">API Documentation</a>
        </body>
    </html>
    """

