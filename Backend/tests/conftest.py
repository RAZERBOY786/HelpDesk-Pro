"""Shared pytest fixtures."""

from __future__ import annotations

import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_app.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-that-is-long-enough-000")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("FRONTEND_ORIGIN", "http://localhost:5173")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core import security
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.enums import UserRole
from app.models.user import User

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture()
def db():
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def make_user(db):
    def _make(
        email: str = "user@example.test",
        password: str = "Password123!",
        role: UserRole = UserRole.EMPLOYEE,
        name: str = "Test User",
        is_active: bool = True,
    ) -> User:
        user = User(
            name=name,
            email=email.lower(),
            password_hash=security.hash_password(password),
            role=role,
            is_active=is_active,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    return _make


@pytest.fixture()
def auth_headers(client):
    def _login(email: str = "user@example.test", password: str = "Password123!") -> dict:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert response.status_code == 200, response.text
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _login
