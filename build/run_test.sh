#!/bin/sh

python -m build.wait_for_postgres
cd source/migrations && alembic upgrade head && cd ../..
pytest -vv -W ignore::DeprecationWarning $@