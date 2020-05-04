import asyncio

from fwork.common.db.postgres.conn_async import db
from fwork.common.db.postgres.settings import DSN
from fwork.common.helpers.utils import retry

if __name__ == '__main__':
    asyncio.run(retry(db.set_bind, bind=DSN))
