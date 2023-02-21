from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .wyres.decoder import Decoder

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/v1/wdp4-push", status_code=204)
async def create_user(request: Request, db: Session = Depends(get_db)):
    raw_content = await request.json()
    decoded_payload = {}
    if 'data' in raw_content:
        decoded_payload = Decoder(payload=raw_content['data'],encoding_format='b64').decode()
    crud.save_content(db,device_id=raw_content['deviceName'], raw_content=raw_content, decoded_payload=decoded_payload)
