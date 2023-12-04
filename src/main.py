from typing import List, Optional, Literal

from fastapi import FastAPI, Path, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from asyncio import sleep
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class Success(BaseModel):
    success: Literal["Success"] = "Success"


class User(BaseModel):
    id: int
    email: str
    is_active: bool
    bio: Optional[str] = None


users: List[User] = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/{user_id}")
def read_user(
    user_id: int = Path(..., description="The ID of the user", gt=2),
    q: str = Query(None, max_length=5),
) -> List[User]:
    matching_users = [user for user in users if user.id == user_id]

    return matching_users if matching_users else []


@app.get("/users")
def read_users():
    return users


@app.post("/users")
def post_item(user: User) -> Literal["Success"]:
    users.append(user)

    return "Success"


@app.get("/events")
async def get_events(request: Request):
    async def event_generator():
        while True:
            # Your logic to wait for or generate data goes here
            # For example, you can query a database or an external API
            # Then yield the data
            yield "data: New event\n\n"
            await sleep(1)  # Wait for a second before the next event

    return StreamingResponse(event_generator(), media_type="text/event-stream")
