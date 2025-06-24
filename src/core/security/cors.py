from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
# ]


def configure_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Or specify domains like ["https://example.com"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
