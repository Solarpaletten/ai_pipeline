#!/usr/bin/env python3
from storage.models import Base
from sqlalchemy import create_engine
from core.config import Config

engine = create_engine(Config.POSTGRES_URL)
Base.metadata.create_all(engine)
print("✅ Database initialized")
