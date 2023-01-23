import importlib
import nest_asyncio
import os
import uvicorn
from api.authentication import router as auth_router
from database.database import init_database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sys import platform

from database.utils import getenv

nest_asyncio.apply()

ENV = getenv('ENV', 'local')
app = None


def init_app():
    app = FastAPI(title='Software Containerization',
                  description='Foobar',
                  docs_url='/docs',
                  openapi_url="/openapi.json",
                  debug=ENV != 'production')

    app.include_router(auth_router, tags=['OAuth2.0'])
    api = importlib.import_module(f'api.api')
    user_api = importlib.import_module(f'api.users')

    app.include_router(api.router, tags=['Todos API'], prefix=f'/todos')
    app.include_router(user_api.router, tags=['Users API'], prefix=f'/users')

    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_credentials=True,
                       allow_methods=['*'],
                       allow_headers=['*'])

    init_database()

    return app


if platform != 'win32' or __name__ == "__main__":
    port = getenv('EXPOSE_PORT', 5008)

    print(f"Starting up app at port {port}...")
    app = init_app()

    print("App initialized")
    uvicorn.run(app, host='0.0.0.0', port=port)