import json
import os.path

import asyncpg
from eme.entities import load_settings, declare_service_type, iter_services

Repository, get_repo = declare_service_type('Repo', 'T')


config = load_settings(os.path.dirname(__file__)+"/ctx.ini")

single_connection = True
pool: asyncpg.Pool | None = None

async def setup_conn(conn):
    def _encoder(value):
        return b'\x01' + json.dumps(value).encode('utf-8')
    def _decoder(value):
        return json.loads(value[1:].decode('utf-8'))
    await conn.set_type_codec('jsonb', encoder=_encoder, decoder=_decoder, schema='pg_catalog', format='binary')
    await conn.set_type_codec('json', encoder=json.dumps, decoder=json.loads, schema='pg_catalog', format='text')

    for repo in iter_services('Repo'):
        if single_connection:
            repo.conn = conn
            # single connection
        #connections.append(conn)

async def initialize_db(pool_size=None):
    global pool, single_connection
    if pool:
        # already initialized
        return

    db = config.get('db.dbhandler')

    min_size, max_size = pool_size if pool_size else config.get(f'{db}.pool_size', cast=lambda x: map(int, x), default=(10, 10))
    single_connection = config.get(f'{db}.single_connection', cast=bool, default=True)

    pool = await asyncpg.create_pool(
        config.get(f'{db}.dsn'),
        min_size=min_size,
        max_size=max_size,
        max_queries=config.get(f'{db}.max_queries', cast=int, default=50000),
        max_inactive_connection_lifetime=config.get(f'{db}.max_inactive_connection_lifetime', cast=float, default=300.0),

        # conn kwargs
        max_cached_statement_lifetime=config.get(f'{db}.max_cached_statement_lifetime', cast=float, default=0),
        init=setup_conn
    )

    if not single_connection:
        for repo in iter_services('Repo'):
            repo.pool = pool

# async def create_connection(dbtype=None):
#     if dbtype is None:
#         dbtype = config.get('db.dbhandler')
#     dbcfg = config[dbtype]
#
#     conn = await asyncpg.connect(dbcfg.pop('dsn'), max_cached_statement_lifetime=0)
#
#     connections.append(conn)


async def close_db():
    if single_connection:
        await pool.close()
    else:
        pass
        # for conn in connections:
        #     await conn.close()
        #
        # connections.clear()

async def get_conn():
    #return connections[0]
    pass
    # async with pool.acquire() as connection:
