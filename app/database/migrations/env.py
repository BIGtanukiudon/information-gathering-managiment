from database.config import DATABASE_URL
from logging.config import fileConfig
import pathlib
import alembic
from sqlalchemy import engine_from_config, pool
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

config = alembic.context.config
fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", str(DATABASE_URL))


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        alembic.context.configure(
            connection=connection,
            target_metadata=None
        )
        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


run_migrations_online()
