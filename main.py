from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return "SUCCESS"


in_memory_dict = {}


def get_value_from_in_memory(key: str):
    global in_memory_dict

    if key in in_memory_dict:
        return in_memory_dict[key]

    return None

def update_value_from_in_memory(key: str, value):
    global in_memory_dict
    in_memory_dict[key] = value


@app.put("/counts/increment/global-variable")
def increment_count():
    count = get_value_from_in_memory("count")
    next_val = count + 1 if count else 1
    update_value_from_in_memory("count", next_val)
    return next_val
