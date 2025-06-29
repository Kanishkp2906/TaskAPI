from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
from config import DB_URL

engine = create_engine(DB_URL, connect_args={'check_same_thread':False}, pool_pre_ping=True)
Sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()