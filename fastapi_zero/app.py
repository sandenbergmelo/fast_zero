from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

database: list[UserPublic] = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)

    return user_with_id


@app.get('/users', response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/users/{id}', response_model=UserPublic)
def get_user_by_id(id: int):
    if id < 1 or id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return database[id - 1]


@app.put('/users/{id}', response_model=UserPublic)
def update_users(id: int, user: UserSchema):
    if id < 1 or id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(id=id, **user.model_dump())
    database[id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{id}', response_model=Message)
def delete_users(id: int):
    if id < 1 or id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[id - 1]

    return {'message': 'User deleted'}
