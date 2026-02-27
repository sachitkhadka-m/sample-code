from sqlmodel import SQLModel,Session, create_engine, select
from fastapi import FastAPI, Depends
from typing import Annotated, List
from models import Hero,Team

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/heroes/")
def read_heroes(session: SessionDep) -> list[Hero]:
    heroes = session.exec(select(Hero)).all()
    return heroes

@app.get('/heroes/{hero_id}')
def read_hero(hero_id: int, session: SessionDep) -> Hero | None:
    hero = session.get(Hero, hero_id)
    return hero

@app.post("/heroes/", response_model=Hero)
def create_hero(*, session: SessionDep, hero: Hero) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if hero:
        session.delete(hero)
        session.commit()
        return {"ok": True}
    return {"ok": False, "error": "Hero not found"}

@app.get("/teams/", response_model=List[Team])
def read_teams(session: SessionDep) -> List[Team]:
    teams = session.exec(select(Team)).all()
    return teams

@app.post("/teams/", response_model=Team)
def create_team(*, session: SessionDep, team: Team) -> Team:
    session.add(team)
    session.commit()
    session.refresh(team)
    return team

