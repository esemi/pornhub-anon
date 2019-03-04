import aioredis

_REDIS_POOL = None

def video_key(video_id: int):
    return 'pornanon:video:%s' % video_id


async def create_conn(loop):
    global _REDIS_POOL
    _REDIS_POOL = await aioredis.create_redis_pool('redis://localhost', minsize=5, maxsize=10, loop=loop)


async def add_video(video_id: int):
    await _REDIS_POOL.hmset_dict(video_key(video_id), {'state': 'loaded'})


async def exist_video(video_id: int) -> bool:
    row = await _REDIS_POOL.hgetall(video_key(video_id), encoding='utf-8')
    return bool(row)


async def fetch_for_processing() -> int:
    pass


async def close_conn():
    global _REDIS_POOL
    _REDIS_POOL.close()
    await _REDIS_POOL.wait_closed()
