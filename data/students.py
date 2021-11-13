from sqlalchemy import Column, Integer, String, BOOLEAN
from data.database import Base


class Student(Base):
    __tablename__ = 'students'

    user_id = Column(Integer, primary_key=True)    #primary_key => первичный ключ
    fio = Column(String)
    user_name = Column(String)
    email = Column(String)
    balance = Column(Integer)
    promo_code = Column(String)
    activations = Column(Integer)
    entered_promo_code = Column(BOOLEAN)

    def __init__(self, user_id: int, fio: str, user_name: str, email: str, given_promo_code: str, balance: int,
                 entered_promo_code: bool):
        self.user_id = user_id
        self.fio = fio
        self.user_name = user_name
        self.email = email
        self.balance = balance
        self.given_promo_code = given_promo_code
        self.activations = 0
        self.entered_promo_code = entered_promo_code

    # def __repr__(self):
    #     return
    #
    #
