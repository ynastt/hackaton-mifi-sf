from aio_pika import connect_robust, Channel
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool
from app.config_reader import config


async def get_connection() -> AbstractRobustConnection:
    return await connect_robust(config.ARMQ_URL)


async def get_channel() -> Channel:
    connection_pool: Pool = Pool(get_connection, max_size=50)
    async with connection_pool.acquire() as connection:
        return await connection.channel()


channel_pool: Pool = Pool(get_channel, max_size=50)
