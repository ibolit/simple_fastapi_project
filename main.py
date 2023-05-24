from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.routing import APIRoute
from pydantic import BaseModel

from typing import Callable
import re
app = FastAPI()


class MyThing(BaseModel):
    name: str
    id: int
    is_required: bool = False
    length: float | None = None


@app.get("/")
def read_root(thing: MyThing) -> MyThing:
    if thing.name == "":
        return thing
    return thing


class MyRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def my_route_handler(request: Request) -> Response:
            body = await request.body()
            if re.match(rb'.*"name"\s*:\s*""', body):
                return Response("ok")
            print(body)
            return await original_route_handler(request)

        return my_route_handler


my_router = APIRouter(route_class=MyRoute)


@my_router.get("/other_thing")
def read_other_thing(_thing: MyThing) -> MyThing:
    return MyThing(name="NoName", id=0)


app.include_router(my_router)
