from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN
from data.database import Base


class Event(Base):
    __tablename__ = 'events'

    number = Column(Integer, primary_key=True)
    name = Column(String)  # primary_key => первичный ключ
    description = Column(String)
    link = Column(String)

    def __init__(self, number: int, name: str, description: str, link: str):
        self.number = number
        self.name = name
        self.description = description
        self.link = link

    def __repr__(self):
        return f'Вебинар №{self.id}, название: {self.name}, ссылка: {self.balance}'