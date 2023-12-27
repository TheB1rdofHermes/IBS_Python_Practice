from fastapi import FastAPI
from typing import List

app = FastAPI()

def find_in_different_registers(words: list[str]) -> list:
    repeat = []
    # Находим слова с дублями по регистру
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if words[i] == words[j]:
                repeat.append(words[i].lower())

    # Приводим все слова к нижнему регистру
    for i in range(len(words)):
        words[i] = words[i].lower()

    # Получаем уникальные слова в нижнем регистре
    words = list(set(words))
    repeat = list(set(repeat))

    # Удаляем повторяющиеся слова из уникальных
    for word in repeat:
        words.remove(word)

    return words

@app.post("/find_in_different_registers", response_model=List[str])
async def get_unique_words(words: List[str]):
    result = find_in_different_registers(words)
    return result
