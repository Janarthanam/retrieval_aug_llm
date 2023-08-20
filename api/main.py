#!/usr/bin/env python3
from fastapi import FastAPI
from routes import search, upload
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from uvicorn.logging import DefaultFormatter
import logging
import uvicorn
from exception import generic_exception_handler

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(DefaultFormatter())
logger.addHandler(handler)

# Create the FastAPI instance
app = FastAPI()
app.include_router(search.router)
app.include_router(upload.router)
app.exception_handler(generic_exception_handler)

app.add_middleware(CORSMiddleware, allow_origins = ["*"],
                   allow_credentials=True,
                   allow_methods=["GET","POST","PUT", "DELETE"],
                   allow_headers = ["*"])

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    print(
        f"{request.method} {request.url.path} {response.status_code} {process_time:.2f}ms"
    )
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
