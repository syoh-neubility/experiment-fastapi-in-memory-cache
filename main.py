from typing import Union, Optional
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

app = FastAPI()


@app.get("/")
async def root():
    return "SUCCESS"


in_memory_dict = {}


async def get_value_from_in_memory(key: str):
    global in_memory_dict

    if key in in_memory_dict:
        return in_memory_dict[key]

    return None


def update_value_from_in_memory(key: str, value):
    global in_memory_dict
    in_memory_dict[key] = value


@app.put("/counts/increment/global-variable")
async def increment_count_global_variable():
    count = get_value_from_in_memory("count")
    next_val = count + 1 if count else 1
    update_value_from_in_memory("count", next_val)
    return next_val


async def get_count():
    return await FastAPICache.get_backend().get("count")


async def update_count(value: int):
    print("update_count called with: ", value)
    return await FastAPICache.get_backend().set("count", value, 100)


@cache(expire=1)
async def expensive_calc():
    print("expensive_calc called")
    return 1 + 1


@app.put("/counts/increment/in-memory-cache")
async def increment_count_in_memory_cache():
    value = await get_count()
    print(value)
    next_value = value + 1 if value else 1
    await update_count(next_value)
    value = await get_count()
    print(value)
    return {"value": next_value, "expensive_calc": await expensive_calc()}


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


def custom_key_builder(
    func,
    namespace: Optional[str] = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    prefix = FastAPICache.get_prefix()
    print(kwargs)
    cache_key = f"{prefix}{kwargs['kwargs']['name']}"
    return cache_key


@cache(expire=100, key_builder=custom_key_builder)
async def get_or_create_user(name, info: Optional[dict] = None):
    return info


@app.post("/users")
async def create_a_user(req_body: dict):
    return await get_or_create_user(name=req_body["name"], info=req_body)


@app.get("/users/{name}")
async def create_a_user(name: str):
    return await get_or_create_user(name=name)
