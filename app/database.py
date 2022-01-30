from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# LOCAL - MYSQL
# SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://{user}:{pw}@{host}/{db}'.format(
#     host=settings.database_hostname,
#     user=settings.database_username,
#     pw=settings.database_password,
#     db=settings.database_name
# )

# HEROKU - POSTGRES
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="root",
#             database='fastapi'
#         )
#         cursor = conn.cursor(dictionary=True)
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Errror: ", error)
#         time.sleep(2)