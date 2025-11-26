from abc import ABC

from fastapi import APIRouter


class APIController(ABC):
    router: APIRouter
