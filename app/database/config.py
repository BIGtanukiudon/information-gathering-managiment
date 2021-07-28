from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config.env as env


DATABASE_URL = f"postgresql://{env.POSTGRES_USER}:{env.POSTGRES_PASSWORD}@{env.POSTGRES_SERVER}:{env.POSTGRES_PORT}/{env.POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
