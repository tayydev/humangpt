import uvicorn

from backend.src import server

if __name__ == "__main__":
    uvicorn.run(server.app, host="127.0.0.1", port=8000)
