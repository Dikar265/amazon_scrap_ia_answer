from typing import Union

from fastapi import FastAPI
from routes import scrap, search
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(scrap.router)
app.include_router(search.router)