#Данный код реализует функцию , выполняющую проверки:
# Проверка 1. Минимальный возраст.
# Если клиент моложе 20 лет – отказ.
# Проверка 2. Проверка действительности паспорта.
# Если возраст клиента более 20 лет и дата выдачи паспорта ранее, чем дата
# достижения им возраста 20 лет, либо если возраст клиента более 45 лет и дата
# выдачи паспорта ранее, чем дата достижения им возраста 45 лет - отказ.
# Проверка 3. Проверка кредитной истории.
# Наличие в кредитной истории в Банке хотя бы одного из условий приводит к
# отказу.
# Если тип кредита не «Кредитная карта», то проверяется:
# 1. Имеется непогашенная просроченная задолженность.
# 2. Возникала просроченная задолженность протяженностью более 60 дней.
# 3. Есть больше двух кредитов с просроченной задолженностью
# протяженностью более 15 дней.
# Если тип кредита «Кредитная карта», то проверяется:
# 1. Имеется непогашенная просроченная задолженность.
# 2. Возникала просроченная задолженность протяженностью более 30 дней.
import json
from datetime import datetime, timedelta


def calculate_age(birth_date):
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def stop_checks(client):
    # Проверка минимального возраста
    birth_date = datetime.fromisoformat(client["birthDate"].replace('Z', '+00:00'))
    age = calculate_age(birth_date)
    if age < 20:
        return False

    # Проверка действительности паспорта
    passport_issued_at = datetime.fromisoformat(client["passport"]["issuedAt"].replace('Z', '+00:00'))
    age_20_date = birth_date + timedelta(days=20 * 365.25)
    age_45_date = birth_date + timedelta(days=45 * 365.25)

    if age >= 20 and passport_issued_at < age_20_date:
        return False
    if age >= 45 and passport_issued_at < age_45_date:
        return False

    # Проверка кредитной истории
    overdue_60 = False
    overdue_15_count = 0

    for credit in client["creditHistory"]:
        if credit["currentOverdueDebt"] > 0:
            return False

        if credit["type"] != "Кредитная карта":
            if credit["numberOfDaysOnOverdue"] > 60:
                overdue_60 = True
            if credit["numberOfDaysOnOverdue"] > 15:
                overdue_15_count += 1
        else:
            if credit["numberOfDaysOnOverdue"] > 30:
                return False

    if overdue_60 or overdue_15_count > 2:
        return False

    return True


# Тестовый JSON
client_json = '''
{
"firstName": "Иван",
"middleName": "Иванович",
"lastName": "Иванов",
"birthDate": "1969-12-31T21:00:00.000Z",
"citizenship": "РФ",
"passport": {
"series": "12 34",
"number": "123456",
"issuedAt": "2023-03-11T21:00:00.000Z",
"issuer": "УФМС",
"issuerСode": "123-456"
},
"creditHistory": [
{
"type": "Кредит наличными",
"currency": "RUB",
"issuedAt": "2003-02-27T21:00:00.000Z",
"rate": 0.13,
"loanSum": 100000,
"term": 12,
"repaidAt": "2004-02-27T21:00:00.000Z",
"currentOverdueDebt": 0,
"numberOfDaysOnOverdue": 0,
"remainingDebt": 0,
"creditId": "25e8a350-fbbc-11ee-a951-0242ac120002"
},
{
"type": "Кредитная карта",
"currency": "RUB",
"issuedAt": "2009-03-27T21:00:00.000Z",
"rate": 0.24,
"loanSum": 30000,
"term": 3,
"repaidAt": "2009-06-29T20:00:00.000Z",
"currentOverdueDebt": 0,
"numberOfDaysOnOverdue": 2,
"remainingDebt": 0,
"creditId": "81fb1ff6-fbbc-11ee-a951-0242ac120002"
},
{
"type": "Кредит наличными",
"currency": "RUB",
"issuedAt": "2009-02-27T21:00:00.000Z",
"rate": 0.09,
"loanSum": 200000,
"term": 24,
"repaidAt": "2011-03-02T21:00:00.000Z",
"currentOverdueDebt": 0,
"numberOfDaysOnOverdue": 14,
"remainingDebt": 0,
"creditId": "c384eea2-fbbc-11ee-a951-0242ac120002"
},
{
"type": "Кредит наличными",
"currency": "RUB",
"issuedAt": "2024-05-15T21:00:00.000Z",
"rate": 0.13,
"loanSum": 200000,
"term": 36,
"repaidAt": null,
"currentOverdueDebt": 10379,
"numberOfDaysOnOverdue": 15,
"remainingDebt": 110000,
"creditId": "ebeddfde-fbbc-11ee-a951-0242ac120002"
}
]
}
'''

client_data = json.loads(client_json)
result = stop_checks(client_data)
print(result)
