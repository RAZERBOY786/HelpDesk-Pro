"""Model metadata base and model registry.

Importing this module registers every model with ``Base.metadata`` so Alembic
autogenerate can detect tables.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models import *  # noqa: E402,F401,F403
import app.models as _models  # noqa: E402,F401