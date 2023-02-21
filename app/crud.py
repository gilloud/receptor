from sqlalchemy.orm import Session

from . import models, schemas

import datetime

def save_content(db: Session, device_id: str, raw_content: schemas.Wdp4EventPushed, decoded_payload: schemas.WyresDecodedPayload):

    db_raw_content = models.RawContent(device_id=device_id, pushed_content=raw_content,decoded_payload=decoded_payload,pushed_timestamp=datetime.datetime.now(),status=0)
    db.add(db_raw_content)
    db.commit()
    db.refresh(db_raw_content)
    return db_raw_content
