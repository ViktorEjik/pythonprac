import asyncio


async def writer(q, delay: int, evant):
    i = 0
    while not evant.is_set():
        await asyncio.sleep(delay)
        await q.put(f'{i}_{delay}')
        i += 1


async def stacker(q, s:list, evant):
    while not evant.is_set():
        obj = await q.get()
        s.append(obj)


async def reader(s: list, count: int, delay: int, evant):
    while count > 0:
        await asyncio.sleep(delay)
        if s:
            print(s.pop())
            count -= 1
    evant.set()


async def main():
    del_1, del_2, del_3, count = eval(input())
    q = asyncio.Queue()
    s = list()
    stop_evant = asyncio.Event()
    await asyncio.gather(
        writer(q, del_1, stop_evant),
        writer(q, del_2, stop_evant),
        stacker(q, s, stop_evant),
        reader(s, count, del_3,stop_evant)
    )


if __name__ == '__main__':
    asyncio.run(main())
