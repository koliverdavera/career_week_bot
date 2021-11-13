from data.database import Session, create_db
from data.students import Student
from data.companies import Company
from data.events import Event


def create_database():
    create_db()



def _load_fake_data(session: Session):
    student = Student(user_id=10101010, fio='Коливерда Вера Александровна',
                      user_name='koli_vera', email='koliverdavera@gmail.com',
                      balance=2, given_promo_code='2K2K2K2K', entered_promo_code=False)
    session.add(student)
    session.commit()
    session.close()