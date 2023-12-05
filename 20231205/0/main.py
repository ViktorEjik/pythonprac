import asyncio

async def prod(q1):
    for i in range(5):
        await q1.put(f'value_{i}')
        print(f'prod:put value_{i} to q1')
        await asyncio.sleep(1)

async def mid(q1, q2):
    while True:
        s = await q1.get()     
        print(f'mid:get {s} from q1')
        await q2.put(s)
        print(f'mid:put {s} to q2')

async def cons(q2):
    while True:
        s = await q2.get()
        print(f'cons:get {s} from q2')
    

async def main():
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()
    await asyncio.gather(prod(q1), mid(q1, q2), cons(q2))

asyncio.run(main())