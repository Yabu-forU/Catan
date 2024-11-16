"""Backend Model-First Database management with schema models."""
import sqlalchemy.dialects.mysql.pymysql
import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    text,
    Sequence,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists, drop_database


USER = "devweb_user_admin"
PASSWORD = "lala"
HOST = "localhost"
PORT = "5432"

# Base de données
# DATABASE_URL = "sqlite:///./test.db"  # Utilisation d'une base de données SQLite pour l'exemple
Base = declarative_base()


# Modèle de la table User
class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email= Column(String)
    motdepasse = Column(String, nullable=False)
    scoreMax = Column(Integer, nullable=True)
    

# Modèle de la table PartieAmis
# class PartieAmisDB(Base):
#     __tablename__ = 'partie_amis'
#     id_partie = Column(Integer, primary_key=True, index=True)
#     idUser1 = Column(Integer, ForeignKey('users.id'), nullable=False)
#     idUser2 = Column(Integer, ForeignKey('users.id'), nullable=False)
#     pointsUser1 = Column(Integer, nullable=True)
#     pointsUser2 = Column(Integer, nullable=True)

# # Fonction pour initialiser la base de données
# def init_db():
#     engine = create_engine(DATABASE_URL)
#     Base.metadata.create_all(bind=engine)
#     return engine

# # Fonction pour obtenir une session
# def get_session(engine):
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     return SessionLocal()


class database_management:
    def __init__(self, db_name: str, recreate: bool):
        self.engine = create_engine(
            f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{db_name}"
        )
        self.db_name = db_name

        if recreate:
            if database_exists(self.engine.url):
                drop_database(self.engine.url)

        if not database_exists(self.engine.url):
            self.create_db()
        if not sqlalchemy.inspect(self.engine).has_table("users"):
            self.create_tables()

    def create_db(self):
        create_database(self.engine.url)
        
    def create_tables(self):
        Base.metadata.create_all(self.engine)
        with self.engine.connect() as conn:
            conn.execute(text("CREATE SEQUENCE IF NOT EXISTS  post_id_seq"))
            conn.execute(text("CREATE SEQUENCE IF NOT EXISTS  user_id_seq"))
            