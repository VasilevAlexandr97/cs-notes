# blocking_vs_nonblocking_async_vs_sync.py

"""
Тема:
- Блокирующие vs неблокирующие операции
- Синхронные vs асинхронные взаимодействия

Этот файл можно запускать напрямую: каждый блок демонстрирует свою модель работы.
"""

# 1) Блокирующая (blocking)
# Модуль X после отправки запроса останавливается и ждёт ответа от модуля Y, не выполняя другой работы.
print("1) Синхронная блокирующая (пример чтения файла)")
with open(__file__, 'r') as f:
    data = f.read()  # блокирует до завершения чтения
print(f"Прочитали этот файл, длина: {len(data)} символов\n")

# 2) Неблокирующая (non-blocking)
# Модуль X отправляет запрос и сразу продолжает работу, не ожидая ответа от Y.
# При этом X и Y не могут быть в одном потоке/процессе, иначе X не смог бы продолжить.
print("2) Синхронная неблокирующая (пример неблокирующего сокета)")
import socket

sock = socket.socket()
sock.setblocking(False)
try:
    sock.connect(("example.com", 80))
except BlockingIOError:
    print("Соединение устанавливается, но не блокирует поток X")

try:
    chunk = sock.recv(1024)
except BlockingIOError:
    chunk = None
print(f"Данные сразу: {chunk}\n")

# 3) Синхронная (synchronous)
# Описывает взаимодействие X и Y: X не продолжит выполнение, пока Y не вернет результат.
print("3) Синхронное взаимодействие (sync_call)")
def sync_call(y_func):
    result = y_func()
    return result

def y_example():
    print("  Y: начала работу")
    return "результат Y"

res = sync_call(y_example)
print(f"Результат sync_call: {res}\n")

# 4) Асинхронная (asynchronous)
# X отправляет задачу Y и сразу продолжает работу, а Y уведомляет X по завершении.
# При этом X и Y не могут быть в одном потоке/процессе.
print("4) Асинхронное неблокирующее взаимодействие (asyncio)")
import asyncio

async def fetch():
    print("  Запрос…")
    await asyncio.sleep(1)
    print("  Ответ получен")
    return "OK"

async def main():
    task1 = asyncio.create_task(fetch())
    task2 = asyncio.create_task(fetch())
    res1 = await task1
    res2 = await task2
    print(f"Результаты: {res1}, {res2}\n")

asyncio.run(main())

"""
Итоговые выводы

Итоги:
- blocking vs non-blocking: про поведение одного модуля/потока — ждёт он или сразу возвращает управление.
- synchronous vs asynchronous: про взаимодействие двух модулей — ждут они друг друга или нет.
- В non-blocking и asynchronous сценариях X и Y всегда в разных потоках/процессах.


Найденное на stackoverflow объяснение:

An example:
Module X: "I".
Module Y: "bookstore".
X asks Y: do you have a book named "c++ primer"?

blocking: before Y answers X, X keeps waiting there for the answer. Now X (one module) is blocking. X and Y are two threads or two processes or one thread or one process? we DON'T know.

non-blocking: before Y answers X, X just leaves there and do other things. X may come back every two minutes to check if Y has finished its job? Or X won't come back until Y calls him? We don't know. We only know that X can do other things before Y finishes its job. Here X (one module) is non-blocking. X and Y are two threads or two processes or one process? we DON'T know. BUT we are sure that X and Y couldn't be one thread.

synchronous: before Y answers X, X keeps waiting there for the answer. It means that X can't continue until Y finishes its job. Now we say: X and Y (two modules) are synchronous. X and Y are two threads or two processes or one thread or one process? we DON'T know.

asynchronous: before Y answers X, X leaves there and X can do other jobs. X won't come back until Y calls him. Now we say: X and Y (two modules) are asynchronous. X and Y are two threads or two processes or one process? we DON'T know. BUT we are sure that X and Y couldn't be one thread.


blocking: OMG, I'm frozen! I can't move! I have to wait for that specific event to happen. If that happens, I would be saved!

non-blocking: I was told that I had to wait for that specific event to happen. OK, I understand and I promise that I would wait for that. But while waiting, I can still do some other things, I'm not frozen, I'm still alive, I can jump, I can walk, I can sing a song etc.

synchronous: My mom is gonna cook, she sends me to buy some meat. I just said to my mom: We are synchronous! I'm so sorry but you have to wait even if I might need 100 years to get some meat back...

asynchronous: We will make a pizza, we need tomato and cheeze. Now I say: Let's go shopping. I'll buy some tomatoes and you will buy some cheeze. We needn't wait for each other because we are asynchronous.

"""
