from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
# from sqlalchemy.orm import relationship

from .database import Base


class RawContent(Base):
    __tablename__ = "wdp4_raw_content"

    id = Column(Integer, primary_key=True)
    device_id = Column(String)
    pushed_content = Column(JSON)
    decoded_payload = Column(JSON)
    pushed_timestamp = Column(DateTime)
    status = Column(Integer)

    def __repr__(self):
        return f"RawContent(id={self.id!r}, pushed_timestamp={self.pushed_timestamp!r}, fullname={self.status!r})"
