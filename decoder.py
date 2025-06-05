import asyncio
from time import perf_counter

import aiohttp

URL = "http://localhost:8080/fragment?id="

async def fetch_fragment(session, id_):
    async with session.get(f"{URL}{id_}") as resp:
        return await resp.json()

async def worker(id_gen, session, results, seen_ids, done_event):
    while not done_event.is_set():
        id_ = next(id_gen)
        if id_ in seen_ids:
            continue
        seen_ids.add(id_)
        try:
            data = await fetch_fragment(session, id_)
            results[data["index"]] = data["text"]
            indexes = sorted(results.keys())
            if indexes == list(range(len(indexes))):
                done_event.set()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Error fetching ID {id_}: {e}")

def id_generator():
    i = 1
    while True:
        yield i
        i += 1

async def main():
    start = perf_counter()
    results = {}
    seen_ids = set()
    done_event = asyncio.Event()
    id_gen = id_generator()

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(worker(id_gen, session, results, seen_ids, done_event))
            for _ in range(20)
        ]
        await done_event.wait()
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    message = ' '.join(results[i] for i in sorted(results))
    elapsed = perf_counter() - start
    print(f"\nPuzzle: {message}")
    print(f"Completed in: {elapsed:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
