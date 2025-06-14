from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, field_validator

app = FastAPI()


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
