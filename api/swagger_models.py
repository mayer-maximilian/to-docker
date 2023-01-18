from pydantic import BaseModel, Field, BaseConfig
from typing import Optional


class ApiDefaultResponseModel(BaseModel):
    """ Model for what a default response from the api looks like. """
    message: str = Field(...)
    data: list = Field(...)


class AddUserSchema(BaseModel):
    """Schema for the data necessary to add a user"""
    username: str = Field(description="Username")
    password: str = Field(description="Password")
    full_name: Optional[str] = Field(default=None, description='Full name')
    email: Optional[str] = Field(default=None, description='Email address')
    disabled: Optional[bool] = Field(default=False, description="Whether the user is disabled")

    class Config(BaseConfig):
        """Example of what a featured result should look like."""
        schema_extra = {
            "example": {
                "username": "test123",
                "password": "foobar",
                "full_name": "Foo Bar",
                "email": "foobar@loremipsum.com",
                "disabled": False
            }
        }


class UpdateUserSchema(BaseModel):
    """Schema for the data necessary to update an existing user"""
    username: str = Field(description="Username")
    full_name: Optional[str] = Field(default=None, description='Full name')
    email: Optional[str] = Field(default=None, description='Email address')
    disabled: Optional[bool] = Field(default=False, description="Whether the user is disabled")

    class Config(BaseConfig):
        """Example of what a featured result should look like."""
        schema_extra = {
            "example": {
                "username": "test123",
                "full_name": "Foo Bar",
                "email": "foobar@loremipsum.com",
                "disabled": False
            }
        }
