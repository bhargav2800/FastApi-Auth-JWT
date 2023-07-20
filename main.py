import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

posts = [
    {
        "id": 1,
        "title": "penguins",
        "text": "Penguins are group of aqatic flightless brids."
    },
    {
        "id": 2,
        "title": "tiger",
        "text": "Tigers are the largest living cat species."
    },
    {
        "id": 3,
        "title": "koalas ",
        "text": "koala is arboreal herbivorous marsupial native to Australia."
    }
]

users = []

app = FastAPI()


# Get - for testing
@app.get("/", tags=["test"])
def greet():
    return {"Hello": "World!"}


# Get Posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data": posts}


# Get single post by {id}
@app.get("/posts/{id}", tags=["posts"])
def get_one_post(id: int):
    if id > len(posts):
        return {
            "error": "Post with this ID does not exists !"
        }
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }


# Post a blog post [A handler for creating a post]
@app.post("/post", dependencies=[Depends(jwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(dict(post))
    return {
        "info": "Post Added!"
    }


# User Signup [Create a new user]
@app.post('/user/signup', tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body()):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details !"
        }
