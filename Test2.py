# Данная  функция реализует выполнение данных проверок :
# Проверки для Автомобиля
# Проверка 1. Минимальный возраст водителя.
# Если клиент моложе 21 года – отказ.
#
# Проверка 2. Проверка действительности водительского удостоверения.
# Если возраст клиента более 21 года и дата выдачи водительского удостоверения ранее, чем дата достижения им возраста 18 лет, либо если возраст клиента более 50 лет и дата выдачи водительского удостоверения ранее, чем дата достижения им возраста 50 лет - отказ.
#
# Проверка 3. Проверка истории вождения.
# Наличие в истории вождения хотя бы одного из условий приводит к отказу.
#
# Если тип нарушения не "Парковочное нарушение", то проверяется:
#
# Имеется непогашенный штраф.
# Возникало нарушение правил дорожного движения с наложением штрафа более 60 дней.
# Есть больше двух нарушений с наложением штрафа протяженностью более 15 дней.
# Если тип нарушения "Парковочное нарушение", то проверяется:
#
# Имеется непогашенный штраф.
# Возникало нарушение парковки с наложением штрафа более 30 дней.
import json
from datetime import datetime, timedelta

def calculate_age(birth_date):
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def stop_checks(client):
    # Проверка 1: Минимальный возраст водителя
    birth_date = datetime.fromisoformat(client["birthDate"].replace('Z', '+00:00'))
    age = calculate_age(birth_date)
    if age < 21:
        return False
    
    # Проверка 2: Проверка действительности водительского удостоверения
    driver_license_issued_at = datetime.fromisoformat(client["driverLicense"]["issuedAt"].replace('Z', '+00:00'))
    age_18_date = birth_date + timedelta(days=18*365.25)
    age_50_date = birth_date + timedelta(days=50*365.25)

    if age >= 21 and driver_license_issued_at < age_18_date:
        return False
    if age >= 50 and driver_license_issued_at < age_50_date:
        return False
    
    # Проверка 3: Проверка истории вождения
    overdue_60 = False
    overdue_15_count = 0

    for violation in client["drivingHistory"]:
        if violation["penalty"] > 0:
            return False
        
        if violation["type"] != "Парковочное нарушение":
            if violation["daysOnOverdue"] > 60:
                overdue_60 = True
            if violation["daysOnOverdue"] > 15:
                overdue_15_count += 1
        else:
            if violation["daysOnOverdue"] > 30:
                return False

    if overdue_60 or overdue_15_count > 2:
        return False

    return True

# Пример тестирования
client_json = '''
{
    "firstName": "Иван",
    "middleName": "Иванович",
    "lastName": "Иванов",
    "birthDate": "2000-01-01T00:00:00.000Z",
    "citizenship": "РФ",
    "driverLicense": {
        "number": "123456",
        "issuedAt": "2018-01-01T00:00:00.000Z",
        "issuer": "ГИБДД",
        "expiryDate": "2028-01-01T00:00:00.000Z"
    },
    "drivingHistory": [
        {
            "type": "Превышение скорости",
            "issuedAt": "2021-05-01T00:00:00.000Z",
            "penalty": 3000,
            "daysOnOverdue": 20,
            "paidAt": "2021-06-01T00:00:00.000Z",
            "penaltyId": "a1b2c3d4e5"
        },
        {
            "type": "Парковочное нарушение",
            "issuedAt": "2022-05-01T00:00:00.000Z",
            "penalty": 1000,
            "daysOnOverdue": 5,
            "paidAt": "2022-05-06T00:00:00.000Z",
            "penaltyId": "f6g7h8i9j0"
        },
        {
            "type": "Проезд на красный свет",
            "issuedAt": "2023-01-01T00:00:00.000Z",
            "penalty": 5000,
            "daysOnOverdue": 45,
            "paidAt": "2023-02-15T00:00:00.000Z",
            "penaltyId": "k1l2m3n4o5"
        }
    ]
}
'''

client_data = json.loads(client_json)
result = stop_checks(client_data)
print(result)  # Ожидаемый результат: True или False в зависимости от проверок
