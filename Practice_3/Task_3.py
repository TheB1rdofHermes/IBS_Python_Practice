from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from databases import Database
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Boolean
)
from typing import List


app = FastAPI()

# Настройки подключения к базе данных SQLite
DATABASE_URL = "sqlite:///./todo.db"
database = Database(DATABASE_URL)

metadata = MetaData()

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("task", String(255)),
    Column("status", Boolean)
)

# Модель для задачи
class Task(BaseModel):
    task: str
    status: bool

# Модель для обновления задачи
class TaskUpdate(BaseModel):
    task: str
    status: bool

# Создание таблицы, если она еще не существует
@app.on_event("startup")
async def startup():
    await database.connect()
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)

# Закрытие соединения с базой данных после завершения работы
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Получение списка задач
@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    """
    Получение задачи по её ID.
    """
    query = tasks.select().where(tasks.c.id == task_id)
    task = await database.fetch_one(query)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Добавление задачи
@app.put("/tasks/", status_code=status.HTTP_200_OK, response_model=List[dict])
async def create_tasks(task_list: List[Task]):
    """
    Добавление списка задач.
    """
    added_tasks = []
    for task in task_list:
        query = tasks.insert().values(task=task.task, status=task.status)
        last_record_id = await database.execute(query)
        added_task = task.dict()
        added_task["task_id"] = last_record_id
        added_tasks.append(added_task)
    return added_tasks


# Удаление задачи
@app.delete("/tasks/{task_id}/", status_code=status.HTTP_200_OK)
async def delete_task(task_id: str):
    """
    Удаление задачи по её ID.
    """
    if not task_id.isdigit():
        raise HTTPException(status_code=424, detail="Invalid task_id. Expecting an integer value.")

    task_id_int = int(task_id)
    query = tasks.delete().where(tasks.c.id == task_id_int)
    deleted = await database.execute(query)

    if deleted:
        return {"detail": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")


# Обновление задачи
@app.post("/tasks/{task_id}/", response_model=Task)
async def update_task(task_id: int, task: TaskUpdate):
    """
    Обновление задачи по её ID.
    """
    query = (
        tasks
            .update()
            .where(tasks.c.id == task_id)
            .values(task=task.task, status=task.status)
    )
    await database.execute(query)

    updated_task = await database.fetch_one(tasks.select().where(tasks.c.id == task_id))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

