import contextlib
import typing

import litestar
import redis.asyncio
from litestar.response import ServerSentEvent


@contextlib.asynccontextmanager
async def create_redis_client() -> typing.AsyncGenerator[redis.asyncio.Redis, None]:
    redis_client = redis.asyncio.Redis(host="localhost", port="6379")
    try:
        await redis_client.initialize()
        print("initialized redis client")
        yield redis_client
    finally:
        await redis_client.aclose()
        print("closed redis client")


redis_list_key = "whatever"


async def _iter_sse_session_events_as_str() -> typing.AsyncIterable[str]:
    async with create_redis_client() as redis_client:
        while True:
            try:
                # BLPOP blocks redis client until an item in list is available,
                # i. e. you can't do anything with the client while waiting here.
                _list_key, event_content = await redis_client.blpop(redis_list_key)
            except BaseException as exception:
                print("caught an exception from blpop:", exception)
                raise exception

            yield event_content


@litestar.get("/sse")
async def listen_to_sse_session_events() -> ServerSentEvent:
    return ServerSentEvent(_iter_sse_session_events_as_str())


app = litestar.Litestar([listen_to_sse_session_events])
