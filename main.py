from typing import Union
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

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


@app.put("/counts/increment/in-memory-cache")
async def increment_count_in_memory_cache():
    value = await get_count()
    print(value)
    next_value = value + 1 if value else 1
    await update_count(next_value)
    value = await get_count()
    print(value)
    return next_value


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")