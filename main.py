import asyncio
import random
from dataclasses import dataclass, field

"""Задача 1. Есть 50 URL. Имитируй запросы через asyncio.sleep(random.uniform(0.5, 4)). 
Максимум 5 запросов одновременно, таймаут каждого — 2 секунды. 
Нужно собрать успешные результаты и список неудачных запросов. 
Программа не должна падать из-за одного таймаута."""

# @dataclass
# class Result:
#     successes: list = field(default_factory=list)
#     failures: list = field(default_factory=list)


# async def fetch(url: str, semaphore: asyncio.Semaphore) -> tuple[str, bool, str | None]:
#     async with semaphore:
#         try:
#             delay = random.uniform(0.5, 4)
#             await asyncio.wait_for(asyncio.sleep(delay), timeout=2.0)
#             return (url, True, None)
#         except asyncio.TimeoutError:
#             return (url, False, "timeout")
#         except Exception as e:
#             return (url, False, str(e))


# async def main():
#     urls = [f"https://example.com/{i}" for i in range(1, 51)]
#     semaphore = asyncio.Semaphore(5)
#     result = Result()

#     tasks = [asyncio.create_task(fetch(url, semaphore)) for url in urls]

#     for coro in asyncio.as_completed(tasks):
#         url, success, error = await coro
#         if success:
#             result.successes.append(url)
#         else:
#             result.failures.append({"url": url, "error": error})

#     print(f"Успешных: {len(result.successes)}, Неудачных: {len(result.failures)}")
#     print("\nПервые 5 неудачных:")
#     for item in result.failures[:5]:
#         print(f"  ✗ {item['url']} — {item['error']}")


# if __name__ == "__main__":
#     asyncio.run(main())

"""Задача 2. Producer / Consumer
Producer создаёт 100 задач с интервалом 0.1 секунды. 
Три Worker обрабатывают каждую за 0.5–2 секунды. 
Используй asyncio.Queue(maxsize=10). 
После обработки всех задач корректно заверши работников и выведи статистику по каждому."""

# @dataclass
# class Stats:
#     processed: int = 0
#     total_time: float = 0.0


# async def producer(queue: asyncio.Queue, count: int = 100):
#     for i in range(1, count + 1):
#         task = f"task-{i}"
#         await queue.put(task)
#         print(f"[producer] положил {task} (в очереди: {queue.qsize()})")
#         await asyncio.sleep(0.1)

#     for _ in range(3):
#         await queue.put(None)

#     print("[producer] завершил работу")


# async def worker(name: str, queue: asyncio.Queue, stats: dict):
#     while True:
#         task = await queue.get()

#         if task is None:
#             queue.task_done()
#             print(f"[{name}] получил сигнал завершения")
#             break

#         try:
#             duration = random.uniform(0.5, 2)
#             await asyncio.sleep(duration)
#             stats[name].processed += 1
#             stats[name].total_time += duration
#             print(f"[{name}] обработал {task} за {duration:.2f}с")
#         finally:
#             queue.task_done()


# async def main():
#     queue = asyncio.Queue(maxsize=10)
#     stats = {f"worker-{i}": Stats() for i in range(1, 4)}

#     producer_task = asyncio.create_task(producer(queue, count=100))

#     workers = [
#         asyncio.create_task(worker(name, queue, stats))
#         for name in stats
#     ]

#     await producer_task
#     await asyncio.gather(*workers)

#     await queue.join()

#     print("\n" + "=" * 40)
#     print("СТАТИСТИКА")
#     print("=" * 40)
#     total = 0
#     for name, s in stats.items():
#         avg = s.total_time / s.processed if s.processed else 0
#         print(f"{name}: обработано={s.processed}, "
#               f"суммарное время={s.total_time:.2f}с, "
#               f"среднее={avg:.2f}с")
#         total += s.processed
#     print(f"Всего обработано: {total}")


# if __name__ == "__main__":
#     asyncio.run(main())

"""Задача 3. Race Condition
Есть общий банковский баланс balance = 1000. 
Одновременно запускаются 100 операций снятия по 10 единиц. 
Искусственно создай race condition с await asyncio.sleep(0) между проверкой и изменением баланса. 
Затем исправь проблему с помощью asyncio.Lock."""

balance = 1000

async def withdraw_broken(amount: int):
    global balance
    if balance >= amount:
        await asyncio.sleep(0)
        balance -= amount
        return True
    return False


async def main():
    global balance
    balance = 1000

    tasks = [asyncio.create_task(withdraw_broken(10)) for _ in range(100)]
    results = await asyncio.gather(*tasks)

    success = sum(results)
    print(f"Успешных снятий: {success}")
    print(f"Итоговый баланс: {balance}")
    print(f"Ожидалось: {1000 - success * 10}")


if __name__ == "__main__":
    asyncio.run(main())