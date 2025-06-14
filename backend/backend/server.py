import time

from fastapi import FastAPI, HTTPException, Request
from prometheus_client import REGISTRY, Counter, Histogram, generate_latest
from pydantic import BaseModel, ValidationError, field_validator
from starlette.responses import Response

app = FastAPI()

# METRICS
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency",
    ["method", "endpoint"],
)

VALIDATION_ERRORS = Counter(
    "validation_errors_total", "Total validation errors", ["endpoint"]
)


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    endpoint = request.url.path
    try:
        response = await call_next(request)
    except Exception:
        REQUEST_COUNT.labels(method, endpoint, 500).inc()

    duration = time.time() - start_time
    REQUEST_LATENCY.labels(method, endpoint).observe(duration)
    REQUEST_COUNT.labels(method, endpoint, response.status_code).inc()

    if response.status_code == 422:
        VALIDATION_ERRORS.labels(endpoint).inc()

    return response


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(REGISTRY), media_type="text/plain")


class Item(BaseModel):
    name: str
    age: int

    @field_validator("name")
    def validate_name(cls, name: str):
        if not name.istitle():
            raise ValueError("Name must be title")
        return name

    @field_validator("age")
    def validate_age(cls, age: int):
        if age < 0 or age > 100:
            raise ValueError("Age must be between 0 and 100")
        return age


@app.post("/")
async def root(item: Item):
    return {"message": f"Hello, {item.name}. You're at {item.age} years old"}


@app.get("/health")
async def health_check():
    return {"message": "Healthy"}


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in errors]
    raise HTTPException(status_code=422, detail=error_messages)
