from fastapi import FastAPI
from app.routes import auth
from app.db.database import engine, Base
from app.routes import predict

#Base.metadata.create_all(bind=engine)
app = FastAPI(title="Garbage classification API")
app.include_router(auth.router)
app.include_router(predict.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status":"API running"}
