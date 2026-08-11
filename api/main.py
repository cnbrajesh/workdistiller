from fastapi import FastAPI

from core.storage import Repository

app = FastAPI(title="Emperor's PoV Work OS")

repo = Repository()


@app.get("/")
def root():
    return {
        "message": "Emperor's PoV Work OS local API",
        "endpoints": [
            "/nodes",
        ],
    }


@app.get("/nodes")
def list_nodes():
    return repo.all_nodes()
