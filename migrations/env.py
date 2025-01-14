import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Подтягиваем логгер из alembic.ini
config = context.config
fileConfig(config.config_file_name)

# Импортируем вашу декларативную Base:
from app.database import Base  # где Base = declarative_base()

# Настраиваем metadata, чтобы autogenerate "видел" модели
target_metadata = Base.metadata

# Берём URL из переменных окружения, если хотите динамически:
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydb")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

def run_migrations_offline():
    # ...
    pass

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
