from fastapi import APIRouter

from fast_zero.custom_types.annotated_types import T_CurrentUser, T_Session
from fast_zero.db.models import Todo
from fast_zero.schemas import TodoPublic, TodoSchema

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, user: T_CurrentUser, session: T_Session):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
