from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def example():
    pass
# TODO:
