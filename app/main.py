from .config import settings
from app.services.temp_manager import create_temp_dir , delete_dir

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temp_dir = create_temp_dir()
    yield
    delete_dir(app.state.temp_dir)
    


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    # lifespan=lifespan
)





app.add_middleware(
    CORSMiddleware, 
    allow_origins = settings.cors_origins,
    allow_credentials = True,
    allow_methods = ["get", "post"],
    allow_headers = ["*"]
)



@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>MetaClean API</title>
        </head>
        <body>
            <h1>PureFile API</h1>
            <p>API for reading and clearing metadata.</p>
            <a href="https://github.com/TalonProbeite/PureFile.git">
                GitHub Repository
            </a>
        </body>
    </html>
    """