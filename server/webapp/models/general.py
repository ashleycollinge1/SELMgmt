"""
This contains all of the 'general' models relating to the flask app
"""
from app.database import Base

class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    user = Column(String)
    description = Column(String)
    datetime_created = Column(DateTime, default=datetime.datetime.utcnow)
    email = Column(String)
    subject = Column(String)
    status = Column(String)
    priority = Column(String)
    responder_id = Column(Integer) # Will be foreign key
    due_by = Column(DateTime)
    attachments = Column(String)
    category = Column(String)
