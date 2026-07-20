from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Projects
from schemas import StackOut, ProjectOut, ProjectCreate
from schemas import StackCreate
from models import Stack
from auth import verify_api_key
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets") #Isso é para arquivos estáticos no back end
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/projects")
def list_users(db: Session = Depends(get_db)):
    return db.query(Projects).all()


@app.post("/stacks", response_model=StackOut, dependencies=[Depends(verify_api_key)])
def create_stack(stack: StackCreate, db: Session = Depends(get_db)):
    new_stack = Stack(name=stack.name, svg_icon=stack.svg_icon)
    db.add(new_stack)
    db.commit()
    db.refresh(new_stack)
    return new_stack

@app.post("/projects", response_model=ProjectOut, dependencies=[Depends(verify_api_key)])
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Projects(title=project.title, description=project.description)

    if project.stack_ids:
        stacks = db.query(Stack).filter(Stack.id.in_(project.stack_ids)).all()

        found_ids = {s.id for s in stacks}
        missing = set(project.stack_ids) - found_ids
        if missing:
            raise HTTPException(status_code=404, detail=f"Stacks não encontradas: {missing}")

        new_project.stacks = stacks

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@app.put("/projects/{project_id}", response_model=ProjectOut, dependencies=[Depends(verify_api_key)])
def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = db.query(Projects).filter(Projects.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    db_project.title = project.title
    db_project.description = project.description

    if project.stack_ids:
        stacks = db.query(Stack).filter(Stack.id.in_(project.stack_ids)).all()

        found_ids = {s.id for s in stacks}
        missing = set(project.stack_ids) - found_ids
        if missing:
            raise HTTPException(status_code=404, detail=f"Stacks não encontradas: {missing}")

        db_project.stacks = stacks
    else:
        db_project.stacks = []  

    db.commit()
    db.refresh(db_project)
    return db_project

@app.delete("/projects/{project_id}", dependencies=[Depends(verify_api_key)])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Projects).filter(Projects.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    db.delete(db_project)
    db.commit()
    return {"detail": "Projeto excluído com sucesso"}   

@app.put("/stacks/{stack_id}", response_model=StackOut, dependencies=[Depends(verify_api_key)])
def update_stack(stack_id: int, stack: StackCreate, db: Session = Depends(get_db)):
    db_stack = db.query(Stack).filter(Stack.id == stack_id).first()

    if not db_stack:
        raise HTTPException(status_code=404, detail="Stack não encontrada")

    db_stack.name = stack.name
    db_stack.svg_icon = stack.svg_icon

    db.commit()
    db.refresh(db_stack)
    return db_stack

@app.delete("/stacks/{stack_id}", dependencies=[Depends(verify_api_key)])
def delete_stack(stack_id: int, db: Session = Depends(get_db)):
    db_stack = db.query(Stack).filter(Stack.id == stack_id).first()

    if not db_stack:
        raise HTTPException(status_code=404, detail="Stack não encontrada")

    db.delete(db_stack)
    db.commit()
    return {"detail": "Stack excluída com sucesso"}
@app.get("/stacks", response_model=list[StackOut])
def list_stacks(db: Session = Depends(get_db)):
    return db.query(Stack).all()