"""A query script shaped like the one that stalled a production roll on 13 Nov.

The host, login and table are placeholders. The guard test runs it as
`uv run python query_script.py`, with and without its time limit and login.
"""

import asyncio

import asyncpg


async def main() -> None:
    conn = await asyncpg.connect(
        host="db.example.rds.amazonaws.com",
        user="app_readonly",
        database="app",
        server_settings={"statement_timeout": "60s"},
    )
    print(await conn.fetchval("select count(*) from tickets"))


asyncio.run(main())
