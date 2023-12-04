from pydantic import BaseModel, StringConstraints, field_validator
from typing import Annotated

# from pytest import raises


class Address(BaseModel):
    sub: str
    main: str


class User(BaseModel):
    name: Annotated[str, StringConstraints(min_length=5, max_length=50)]
    age: int
    address: Address

    @field_validator("age")
    def check_age(cls, value):
        if value < 0:
            raise ValueError(f"TEST {value}")


test_user_json = {
    "name": "test1234",
    "age": 20,
    "address": {"sub": "Gangnam", "main": "Seoul"},
}

import logging


def test_pydantic():
    alice: User = User(
        name="test1234",
        age=20,
        address=Address(
            sub="Gangnam",
            main="Seoul",
        ),
    )

    logging.info(alice.model_dump())
    logging.info(alice.parse_raw())

    assert alice == User(**test_user_json)
