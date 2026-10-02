from typing import Dict, Optional
from pydantic import BaseModel, Field


class Credentials(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: Optional[str] = Field(default=None, max_length=256)
    cookies: Optional[Dict[str, str]] = None
    captcha: Optional[str] = Field(default=None, max_length=20)
    cdigest: Optional[str] = Field(default=None, max_length=128)


class LoginCredentials(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=256)
    cookies: Optional[Dict[str, str]] = None
    captcha: Optional[str] = Field(default=None, max_length=20)
    cdigest: Optional[str] = Field(default=None, max_length=128)


class PortalCredentials(BaseModel):
    username: Optional[str] = Field(default=None, max_length=100)
    password: Optional[str] = Field(default=None, max_length=256)
    cookies: Optional[Dict[str, str]] = None
    captcha: Optional[str] = Field(default=None, max_length=20)
    cdigest: Optional[str] = Field(default=None, max_length=128)
    telemetry: Optional[str] = Field(default=None, max_length=2048)


class DualLoginCredentials(BaseModel):
    # Portal Credentials (for Marks & Attendance & Profile)
    portal_username: Optional[str] = Field(default=None, max_length=100)
    portal_password: Optional[str] = Field(default=None, max_length=256)
    portal_captcha: Optional[str] = Field(default=None, max_length=20)
    portal_cdigest: Optional[str] = Field(default=None, max_length=128)
    portal_cookies: Optional[Dict[str, str]] = None

    # Academia Credentials (for Timetable, Courses, Calendar & Profile)
    academia_username: Optional[str] = Field(default=None, max_length=100)
    academia_password: Optional[str] = Field(default=None, max_length=256)
    academia_captcha: Optional[str] = Field(default=None, max_length=20)
    academia_cdigest: Optional[str] = Field(default=None, max_length=128)
    academia_cookies: Optional[Dict[str, str]] = None
