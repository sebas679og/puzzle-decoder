import asyncio
from time import perf_counter

import aiohttp

URL = "http://localhost:8080/fragment?id="

async def fetch_fragment(session, id_):
    async with session.get(f"{URL}{id_}") as resp:
        return await resp.json()

async def worker(id_gen, session, results, done_event, last_update):
    while not done_event.is_set():
        id_ = next(id_gen)
        try:
            data = await fetch_fragment(session, id_)
            if data["index"] not in results:
                results[data["index"]] = data["text"]
                last_update[0] = perf_counter()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Error fetching ID {id_}: {e}")

async def completion_checker(results, done_event, last_update):
    await asyncio.sleep(0.1)
    
    while not done_event.is_set():
        await asyncio.sleep(0.05)
        
        if not results:
            continue
            
        time_since_update = perf_counter() - last_update[0]
        if time_since_update > 0.2:
            indexes = sorted(results.keys())
            if indexes == list(range(len(indexes))) and len(indexes) > 0:
                done_event.set()
                break

def id_generator():
    i = 1
    while True:
        yield i
        i += 1

async def main():
    start = perf_counter()
    results = {}
    done_event = asyncio.Event()
    last_update = [perf_counter()]
    id_gen = id_generator()

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(worker(id_gen, session, results, done_event, last_update))
            for _ in range(30)
        ]

        checker = asyncio.create_task(completion_checker(results, done_event, last_update))
        
        await done_event.wait()

        for task in tasks + [checker]:
            task.cancel()
        await asyncio.gather(*tasks, checker, return_exceptions=True)

    message = ' '.join(results[i] for i in sorted(results))
    elapsed = perf_counter() - start
    print(f"\nPuzzle: {message}")
    print(f"Completed in: {elapsed:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())
