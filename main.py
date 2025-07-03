from fastapi import FastAPI

from pydantic import BaseModel
from typing import Optional

from typing import Union


app = FastAPI()


@app.get("/blogs")
def blogslist(limit= 10, published: bool = True, sort: str = "newest"):
    if published:
        return {"data": f"{limit} is the blogs of that number. And It is {published}"}
    else:
        return {"data": "This is the blogs section of no blogs"}


@app.get("/blogs/unpublished")
def unpublished_blogs():
    return {"data": {"his is the unpublished blogs section"}}

@app.get("/blogs/{id}")
def eachblog(id:int):
    return {"data": "This is the blogs associate with id " + str(id)}


# body request 
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None


@app.post("/blogs")
def create_blog(blog: Blog):
    return {"data": "Blog created successfully", "blog": blog}
