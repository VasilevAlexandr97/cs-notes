"""
shallow_vs_deepcopy.py

Тема: Поверхностное (shallow) и глубокое (deep) копирование в Python

---

🔹 Основные определения:

- **Shallow copy** — поверхностная копия:
  Копируется только сам объект, но вложенные объекты (ссылки) остаются общими.

- **Deep copy** — глубокая копия:
  Рекурсивно копируются все вложенные объекты — создаются независимые дубликаты.

Используются из модуля `copy`:

    from copy import copy, deepcopy
"""

# 🔹 Пример с примитивами (immutable):

from copy import copy, deepcopy


class A:
    def __init__(self, x):
        self.x = x

a = A(1)
b = copy(a)
print(f"b.x до изменения: {b.x}")  # 1

a.x = 2
print(f"b.x после изменения a.x: {b.x}")  # 2 — потому что x — immutable, но ссылка была общая

c = deepcopy(a)
print(f"c.x после deepcopy: {c.x}")  # 2

a.x = 3
print(f"c.x после изменения a.x: {c.x}")  # 2 — deepcopy создал новый объект

"""
В этом примере не видно сильной разницы, так как поле `x` — это число (immutable).
Чтобы увидеть поведение глубже, используем mutable-объекты, например список.
"""

print("\n---\n")

# 🔹 Пример с вложенными mutable-объектами:

class B:
    def __init__(self, data):
        self.data = data  # список — изменяемый объект

original = B([1, 2])
shallow = copy(original)
deep = deepcopy(original)

# Изменим вложенный список
original.data.append(3)

print(f"original.data: {original.data}")   # [1, 2, 3]
print(f"shallow.data: {shallow.data}")     # [1, 2, 3] — shallow копия указывает на тот же список
print(f"deep.data: {deep.data}")           # [1, 2] — deep копия полностью независима

"""

# 🧠 Заключение:

- Shallow copy удобно использовать, когда структура не содержит вложенных изменяемых объектов.
- Deep copy необходим, если нужно создать полностью независимую копию, включая все уровни вложенности.
- Будь осторожен при копировании сложных структур (например, графов или объектов с циклическими ссылками).

"""