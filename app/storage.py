import aioredis

_REDIS_POOL = None


def video_key(video_id: int) -> str:
    return 'pornanon:video:%s' % video_id


def processing_queue_key() -> str:
    return 'pornanon:processing:queue'


async def create_conn(loop):
    global _REDIS_POOL
    _REDIS_POOL = await aioredis.create_redis_pool('redis://localhost', minsize=5, maxsize=10, loop=loop)


async def add_video(video_id: int):
    await _REDIS_POOL.hmset_dict(video_key(video_id), {'state': 'loaded'})
    await _REDIS_POOL.sadd(processing_queue_key(), video_id)


async def update_video_state(video_id: int, faces_count: int):
    await _REDIS_POOL.hmset_dict(video_key(video_id), {'state': 'processed', 'faces': faces_count})


async def exist_video(video_id: int) -> bool:
    row = await _REDIS_POOL.hgetall(video_key(video_id), encoding='utf-8')
    return bool(row)


async def fetch_for_processing() -> int:
    return await _REDIS_POOL.spop(processing_queue_key())


async def close_conn():
    global _REDIS_POOL
    _REDIS_POOL.close()
    await _REDIS_POOL.wait_closed()
