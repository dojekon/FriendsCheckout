def collect_trip_data():
    participants = input("Введите имена участников через запятую: ").split(',')
    participants = [name.strip() for name in participants]
    
    places = input("Введите названия мест через запятую: ").split(',')
    places = [place.strip() for place in places]
    
    orders = {place: {name: [] for name in participants} for place in places}
    shared_expenses = {place: 0 for place in places}
    payers = {place: "" for place in places}

    for place in places:
        print(f"\nСбор данных для {place}:")
        for name in participants:
            print(f"\nВведите заказы для {name} в {place} (формат 'блюдо стоимость'; 'конец' для завершения):")
            while True:
                entry = input()
                if entry.lower() == 'конец':
                    break
                try:
                    dish, cost = entry.rsplit(' ', 1)
                    cost = float(cost)  # Проверяем, что стоимость можно преобразовать в число
                    orders[place][name].append((dish, cost))
                except ValueError:
                    print("Ошибка: введите название и стоимость блюда, разделенные пробелом. Стоимость должна быть числом.")
                    continue
        
        while True:
            shared_entry = input(f"Введите общее блюдо и его стоимость для {place}, или 'нет', если его нет: ")
            if shared_entry.lower() == 'нет':
                break
            try:
                shared_dish, shared_cost = shared_entry.rsplit(' ', 1)
                shared_cost = float(shared_cost)
                shared_expenses[place] = shared_cost
                break
            except ValueError:
                print("Ошибка: введите название и стоимость общего блюда, разделенные пробелом. Стоимость должна быть числом.")

        payer = input(f"Кто оплатил в {place}? ")
        payers[place] = payer

    return participants, places, orders, shared_expenses, payers


def calculate_individual_and_shared_expenses(participants, places, orders, shared_expenses, payers):
    # Словарь для хранения индивидуальных расходов каждого участника по местам
    individual_expenses = {name: {place: sum(cost for _, cost in orders[place][name]) for place in places} for name in participants}
    
    # Словарь для хранения долгов между участниками
    debts = []

    for place in places:
        total_shared_expense = shared_expenses[place]
        total_place_expense = sum(individual_expenses[name][place] for name in participants) + total_shared_expense
        shared_expense_per_person = total_shared_expense / len(participants) if total_shared_expense else 0

        for name in participants:
            individual_expenses[name][place] += shared_expense_per_person  # Добавляем долю общих расходов к индивидуальным
            
        payer_expense = total_place_expense
        for name in participants:
            if name != payers[place]:
                # Сумма, которую должен каждый участник плательщику
                debt_amount = individual_expenses[name][place]
                debts.append((name, payers[place], place, debt_amount))
                payer_expense -= debt_amount
        
        # Корректировка долга плательщика
        individual_expenses[payers[place]][place] = payer_expense

    return debts

def generate_detailed_report(debts, filename="detailed_expenses_report.txt"):
    with open(filename, 'w') as file:
        for debtor, creditor, place, amount in debts:
            file.write(f"{debtor} должен {creditor} {amount:.2f} руб. за {place}\n")
    print(f"Отчет сохранен в файле {filename}.")

# Здесь должен быть код функций collect_trip_data() и main(), которые вы уже видели ранее

def main():
    participants, places, orders, shared_expenses, payers = collect_trip_data()
    debts = calculate_individual_and_shared_expenses(participants, places, orders, shared_expenses, payers)
    generate_detailed_report(debts)

if __name__ == "__main__":
    main()