from fastapi import FastAPI

from .routes import appointments, medspas, services


app = FastAPI()
app.include_router(medspas.router)
app.include_router(services.router)
app.include_router(appointments.router)


@app.get("/")
async def root():
    return {"message": "Hello Moxie"}
