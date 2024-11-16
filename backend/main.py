"""Backend FastAPI Server with REST models."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from db_management import database_management, UserDB
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import Optional
origins = ["http://localhost:3000"]
from fastapi.middleware.cors import CORSMiddleware

import os
import random

def fichier_aleatoire():
    
    dossier = os.path.abspath(os.path.join(__file__, '../..', 'classifai-frontend/public/img'))
    fichiers = os.listdir(dossier)
    fichiers = [f for f in fichiers if os.path.isfile(os.path.join(dossier, f))]
    fichier_choisi = random.choice(fichiers)
    
    return {'source': fichier_choisi,  'isPanier': fichier_choisi.find('panier')!=-1}

app = FastAPI()

app.add_middleware(
   CORSMiddleware, allow_origins=origins, allow_credentials=True,   allow_methods=["*"], allow_headers=["*"],)

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    motdepasse: str
    scoreMax: Optional[int] = 0
    class Config:
        orm_mode = True
class UserScore(BaseModel):
    id: int
    scoreMax: int = 0

dm = database_management("project_database", recreate=False)

def find_user(username: str, session: Session):
    stm = select(UserDB).where(
        UserDB.username == username
    )
    res = session.execute(stm) 
    found_user = res.scalar()

    return found_user
def find_user_by_id(id: int, session: Session):
    stm = select(UserDB).where(
        UserDB.id == id
    )
    res = session.execute(stm) 
    found_user = res.scalar()

    return found_user

@app.get("/users/{username}")
async def get_user(username: str):
    print(type(username),1234567)
    with Session(dm.engine) as session:
        user = find_user(username=username, session=session)
        if user is None:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
        return user



@app.get("/users")
def get_users():
    with Session(dm.engine) as session:
        users = session.query(UserDB).all()
        return users
@app.get("/podium")
def get_users():
    with Session(dm.engine) as session:
        users = session.query(UserDB).order_by(desc(UserDB.scoreMax)).all() 
    return users

@app.get("/image")
def get_image():
    image = fichier_aleatoire()
    return image
    


                
@app.post("/users")
def add_user(user: User):
    print(user)
    with Session(dm.engine) as session:
        found_user : UserDB|None =   None #find_user(user.username, session)
        if found_user is not None:
            return found_user
        else:

            new_user = UserDB(
                username=user.username,
                motdepasse=user.motdepasse,
                email=user.email,
                scoreMax=user.scoreMax,
                
            )
            
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        return user


@app.put("/users")
def put_user(user: User):
    with Session(dm.engine) as session:
        found_user = find_user_by_id(user.id, session)
        found_user.email = user.email
        found_user.motdepasse = user.motdepasse
        found_user.username = user.username
        session.commit()
@app.put("/userScore")
def put_user(user: UserScore):
    with Session(dm.engine) as session:
        found_user = find_user_by_id(user.id, session)
        found_user.scoreMax = user.scoreMax
        session.commit()


@app.delete("/users/{username}")
def delete_user(username):
    with Session(dm.engine) as session:
        found_user = find_user(username, session)
        if found_user is not None:
            session.commit()
        else:
            raise HTTPException(404, "User not found")

# # Routes pour les utilisateurs
# @app.post("/users")
# def create_user(user: User, db: Session = Depends(get_db)):
#     db_user = UserSQL(username=user.username, motdepasse=user.motdepasse, scoreMax=user.scoreMax)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @app.put("/users/{user_id}", response_model=User)
# def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
#     db_user = db.query(UserSQL).filter(UserSQL.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Mettre à jour les attributs de l'utilisateur
#     db_user.username = user.username
#     db_user.motdepasse = user.motdepasse
#     db_user.scoreMax = user.scoreMax

#     db.commit()  # Valider les changements dans la base de données
#     db.refresh(db_user)  # Rafraîchir l'instance de l'utilisateur pour inclure les changements
#     return db_user

# @app.get("/users/{user_id}", response_model=User)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(UserSQL).filter(UserSQL.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @app.get("/users/")
# def get_user( db: Session = Depends(get_db)):
#     user = db.query(UserSQL).all()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
# # @app.get("/users")
# # def get_users():
# #     with Session(dm.engine) as session:
# #         users = session.query(UserDB).all()
# #         return users
    
# @app.delete("/users/{user_id}")
# def delete_user(user_id: int, db: Session =Depends(get_db)):
#     user = db.query(UserSQL).filter(UserSQL. id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return {"message": "User deleted successfully"}

# # Routes pour les parties
# @app.post("/parties", response_model=PartieAmis)
# def create_partie(partie: PartieAmis, db: Session = Depends(get_db)):
#     db_partie = PartieAmisSQL(
#         idUser1=partie.idUser1,
#         idUser2=partie.idUser2,
#         pointsUser1=partie.pointsUser1,
#         pointsUser2=partie.pointsUser2
#     )
#     db.add(db_partie)
#     db.commit()
#     db.refresh(db_partie)
#     return db_partie

# @app.get("/parties/{partie_id}", response_model=PartieAmis)
# def get_partie(partie_id: int, db: Session = Depends(get_db)):
#     partie = db.query(PartieAmisSQL).filter(PartieAmisSQL.id_partie == partie_id).first()
#     if not partie:
#         raise HTTPException(status_code=404, detail="Partie not found")
#     return partie

# @app.delete("/parties/{partie_id}")
# def delete_partie(partie_id: int, db: Session = Depends(get_db)):
#     partie = db.query(PartieAmisSQL).filter(PartieAmisSQL.id_partie == partie_id).first()
#     if not partie:
#         raise HTTPException(status_code=404, detail="Partie not found")
#     db.delete(partie)
#     db.commit()
#     return {"message": "Partie deleted successfully"}
