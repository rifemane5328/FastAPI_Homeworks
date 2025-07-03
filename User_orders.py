import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List


app = FastAPI(
    docs_url="/swagger",
    redoc_url="/redoc",
    title="Users and orders",
    version="0.0.1"
)


class Order(BaseModel):
    id: int = Field(1, ge=1, description="id замовлення")
    quantity: int = Field(1, ge=1, description="кількість продуктів")
    price: float = Field(ge=0.5, description="ціна 1 продукту")


class User(BaseModel):
    id: int = Field(1, ge=1, description="id користувача")
    username: str = Field(description="нікнейм користовача")
    email: EmailStr = Field("@default.com", description="е-пошта")
    password: str = Field(min_length=8, max_length=20, description="пароль")
    orders_list: List[Order] = Field(description="список замовлень")


users: List[User] = [
    User(
        id=1,
        username="danya692",
        email="danyl9821@gmail.com",
        password="danin_password0425",
        orders_list=[
            Order(
                id=1,
                quantity=3,
                price=15
            ),
            Order(
                id=2,
                quantity=6,
                price=30
            )
        ]
    )
]


@app.post("/create_user", response_model=List[User])
def create_new_user(new_user: User):
    users.append(new_user)
    return users


@app.get("/get_user", response_model=User)
async def get_user_info(mail: str):
    for user in users:
        if user.email == mail:
            return user
        raise HTTPException(status_code=404, detail="Користувача з таким e-mail не існує.Спробуйте інший")


if __name__ == "__main__":
    uvicorn.run(app, port=8003)
