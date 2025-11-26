from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.shared.decorators.api.api import API
from modules.shared.exceptions.application_exception import ApplicationException
from modules.shared.exceptions.handlers.application_exception_handler import (
    application_exception_handler,
)
from modules.shared.middleware.correlation_middleware import CorrelationMiddleware

app = FastAPI()
API.initialize(app)


app.add_exception_handler(ApplicationException, application_exception_handler)
app.add_middleware(CorrelationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return {"message": "Microservice Payment is running"}
