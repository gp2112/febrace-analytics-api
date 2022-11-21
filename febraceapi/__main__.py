import uvicorn
import os

PORT = os.environ.get('FEBRACEAPI_PORT', '5000')


def main():
    uvicorn.run("febraceapi:app", host="localhost", port=PORT, log_level="info")
