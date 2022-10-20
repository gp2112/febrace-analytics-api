import uvicorn


def main():
    uvicorn.run("febraceapi:app", port="5000", log_level="info")
