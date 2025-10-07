from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker


#---------create engine-----------#
sqlite_file_name = "expense.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

class Base(DeclarativeBase):
    pass

SessionLocal  = sessionmaker(expire_on_commit=False, autoflush=True, bind=engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()