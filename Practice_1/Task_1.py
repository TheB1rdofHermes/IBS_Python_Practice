from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd

app = FastAPI()

CHECK_LIST = ['Имя', 'Возраст', 'Должность']

# Функция для проверки расширения файла
def validate_csv_file(file):
    return file.endswith('.csv')

# Функция для проверки столбцов в файле
def validate_csv_data(data):
    return all(column in data.columns for column in CHECK_LIST)

@app.post('/average_age_by_position')
def avg_age_by_position(file: UploadFile = File(...)):
    try:
        # Чтение CSV-файла в DataFrame
        employee_data = pd.read_csv(file.file, encoding='cp1251', delimiter=',')
    except Exception as e:
        # Обработка ошибки чтения файла
        raise HTTPException(status_code=400, detail=f"Ошибка при чтении файла: {e}")

    # Проверка соответствия формата файла и наличия необходимых столбцов
    if not validate_csv_file(file.filename) or not validate_csv_data(employee_data):
        raise HTTPException(status_code=400, detail="Неверный формат файла или невалидные данные")

    # Преобразование столбца 'Возраст' к числовому типу данных, игнорируя ошибки (если они есть)
    employee_data['Возраст'] = pd.to_numeric(employee_data['Возраст'], errors='coerce')

    # Проверка наличия данных для расчета среднего возраста
    if employee_data.empty:
        raise HTTPException(status_code=400, detail="Нет данных для расчета среднего возраста")

    # Группировка данных по должности, вычисление среднего возраста и формирование словаря
    employee_dict = employee_data.groupby('Должность')['Возраст'].mean().to_dict()

    # Замена NaN на null в словаре для корректного представления результата
    employee_dict = {key: (value if pd.notnull(value) else None) for key, value in employee_dict.items()}

    return {"status": 200, "data": employee_dict}
