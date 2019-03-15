from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database import *

engine = create_engine('sqlite:///samsung.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
session.query(SeriesName).delete()
session.query(SerType).delete()
session.query(User).delete()
User1 = User(
    name="sai akhil",
    email="saiakhil.031@gmail.com",
    picture="/")
session.add(User1)
session.commit()
print('The user is successfully added!!!')
# creating company names
ser1 = SeriesName(name="J ", user_id=1)
session.add(ser1)
session.commit()
ser2 = SeriesName(name="A ", user_id=1)
session.add(ser2)
session.commit()
ser3 = SeriesName(name="M ", user_id=1)
session.add(ser3)
session.commit()
ser4 = SeriesName(name="S ", user_id=1)
session.add(ser4)
session.commit()
ser5 = SeriesName(name="NOTE ", user_id=1)
session.add(ser5)
session.commit()
ser6 = SeriesName(name="TAB ", user_id=1)
session.add(ser6)
session.commit()
ser7 = SeriesName(name="ON ", user_id=1)
session.add(ser7)
session.commit()
# creating subjects
phone1 = SerType(
    name='J6',
    color='BLUE',
    ram='4GB',
    memory='64GB',
    frontcamera='8 mp',
    rearcamera='13 mp',
    price='16,700',
    screen='5.6 inches',
    slink='https://goo.gl/qfpCpq',
    date=datetime.datetime.now(),
    sernameid=1,
    user_id=1)
session.add(phone1)
session.commit()
phone2 = SerType(
    name='A7',
    color='BLUE',
    ram='6GB',
    memory='128GB',
    frontcamera='24mp',
    rearcamera='24+5+8mp',
    price='22990',
    screen='6inches',
    slink='https://goo.gl/MpAo6V',
    date=datetime.datetime.now(),
    sernameid=2,
    user_id=1)
session.add(phone2)
session.commit()
phone3 = SerType(
    name='M20',
    color='gold',
    ram='4GB',
    memory='64GB',
    frontcamera='8mp',
    rearcamera='13mp',
    price='12990',
    screen='6.3 inches',
    slink='https://goo.gl/1GcMko',
    date=datetime.datetime.now(),
    sernameid=3,
    user_id=1)
session.add(phone3)
session.commit()
phone4 = SerType(
    name='S10',
    color='Black',
    ram='8GB',
    memory='128GB',
    frontcamera='10mp',
    rearcamera='16+12+12mp',
    price='66900',
    screen='6.1 inches',
    slink='https://goo.gl/A5nN2T',
    date=datetime.datetime.now(),
    sernameid=4,
    user_id=1)
session.add(phone4)
session.commit()
phone5 = SerType(
    name='NOTE 8',
    color='Maple gold',
    ram='6GB',
    memory='64GB',
    frontcamera='8mp',
    rearcamera='12+12mp',
    price='74690',
    screen='6.3 inches',
    slink='https://goo.gl/qKW61k',
    date=datetime.datetime.now(),
    sernameid=5,
    user_id=1)
session.add(phone5)
session.commit()
phone6 = SerType(
    name='TAB s4',
    color='Grey',
    ram='4GB',
    memory='64GB',
    frontcamera='8mp',
    rearcamera='13mp',
    price='62700',
    screen='10.5inches',
    slink='https://goo.gl/1Xz5g3',
    date=datetime.datetime.now(),
    sernameid=6,
    user_id=1)
session.add(phone6)
session.commit()
phone7 = SerType(
    name='ON 7',
    color='Black',
    ram='4GB',
    memory='64GB',
    frontcamera='13mp',
    rearcamera='13mp',
    price='14999',
    screen='5.5inches',
    slink='https://goo.gl/TsHN6F',
    date=datetime.datetime.now(),
    sernameid=7,
    user_id=1)
session.add(phone7)
session.commit()
print("Subjects are added succesfully")
