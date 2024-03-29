"""Main of todo app
"""

import math

from loguru import logger

from fastapi import FastAPI, Request, Depends, Form, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from database import init_db, get_db, Session
import models

init_db()

# pylint: disable=invalid-name
templates = Jinja2Templates(directory="templates")

app = FastAPI()

logger = logger.opt(colors=True)
# pylint: enable=invalid-name

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home(request: Request, database: Session = Depends(get_db), limit: int = 15, skip: int = 0):
    """Main page with todo list
    """
    logger.info("In home")
    todos = database.query(models.Todo).order_by(models.Todo.id.desc())

    count = database.query(models.Todo).count()
    pages = math.ceil(count / limit)

    if skip > pages:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("index.html", {"request": request, "todos": todos, "page": skip, "pages": pages, "limit": limit})


@app.get("/complete/{todo_id}")
async def todo_add(todo_id: int, database: Session = Depends(get_db)):
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    logger.info(f"Complete: {todo}")
    todo.completed = True
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/uncomplete/{todo_id}")
async def todo_add(todo_id: int, database: Session = Depends(get_db)):
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    logger.info(f"Uncomplete: {todo}")
    todo.completed = False
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.post("/add")
async def todo_add(request: Request, title: str = Form(default="None"), task: str = Form(default="0 details"), database: Session = Depends(get_db)):
    """Add new todo
    """
    if title == "None":
        return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
    if len(title) > 500:
        return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

    todo = models.Todo(task=task, title = title)
    logger.info(f"Creating todo: {todo}")
    database.add(todo)
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/edit/{todo_id}")
async def todo_get(request: Request, todo_id: int, database: Session = Depends(get_db)):
    """Get todo
    """
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo_list = database.query(models.Todo)
    maintag = todo.tag
    count = 0
    logger.info(f"Editting todo: {todo}")
    for todos in todo_list:
        if todos.tag == maintag:
            count += 1
    logger.info(f"Getting todo: {count}")
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo, "tags": models.Tags, "count": count})


@app.post("/edit/{todo_id}")
async def todo_edit(
        request: Request,
        todo_id: int,
        task: str = Form(...),
        title: str = Form(...),
        completed: bool = Form(False),
        tag: str = Form(None),
        database: Session = Depends(get_db)):
    """Edit todo
    """
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.task = task
    todo.title = title
    todo.completed = completed
    todo.tag = tag
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{todo_id}")
async def todo_delete(request: Request, todo_id: int, database: Session = Depends(get_db)):
    """Delete todo
    """
    try:
        todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
        logger.info(f"Deleting todo: {todo}")
        database.delete(todo)
        database.commit()
        return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
    except Exception:
        return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
