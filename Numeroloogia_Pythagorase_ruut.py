import tkinter as tk
from tkinter import messagebox
import smtplib, ssl
from email.message import EmailMessage
from datetime import datetime
import re

def validate_date(date_text):   # Проверяет корректность формата даты с использованием datetime.strptime.
    try:
        datetime.strptime(date_text, '%d.%m.%Y')
        return True
    except ValueError:
        return False

def validate_email(email):  # Проверяет корректность адреса электронной почты с использованием регулярного выражения.
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def calculate_pythagoras():     # Основная функция для вычислений. Проверяет валидность введенной даты и электронной почты.
    birth_date = entry_date.get()
    name = entry_name.get()
    email = entry_email.get()
    
    if not validate_date(birth_date):   # Проверка корректности введенной даты.
        messagebox.showerror("Ошибка", "Введите дату в формате (дд.мм.гггг)")
        return
    
    if not validate_email(email):   # Проверка корректности введенного адреса электронной почты.
        messagebox.showerror("Ошибка", "Введите корректный адрес электронной почты")
        return
    
    try:
        day, month, year = map(int, birth_date.split("."))  # Разделение даты на день, месяц и год.
        
        # Вычисление рабочих чисел.
        first_work_number = sum(int(digit) for digit in str(day) + str(month))
        second_work_number = sum(int(digit) for digit in str(year))
        p1 = day // 10
        third_work_number = sum(int(digit) for digit in str(first_work_number - 2 * p1))
        fourth_work_number = sum(int(digit) for digit in str(third_work_number))
        
        # Формирование строк для матрицы.
        matrix_row1 = str(day) + str(month) + str(year)
        matrix_row2 = str(first_work_number) + str(second_work_number) + str(third_work_number)
        matrix_row3 = str(third_work_number) + str(fourth_work_number)
        result = (f"Имя: {name}\n"
                  f"Первый ряд чисел: {matrix_row1}\n"
                  f"Второй ряд чисел: {matrix_row2}\n"
                  f"Третий ряд чисел: {matrix_row3}")
        messagebox.showinfo("Квадрат Пифагора", result)
        
        # Сохранение данных в файл.
        with open("Sünnipäev; Numbrid.txt", "a", encoding="utf-8") as file:
            file.write(f"Имя: {name}; Дата рождения: {birth_date}; Числа: {matrix_row1}, {matrix_row2}, {matrix_row3}\n")
        
        # Отправка характеристик на почту.
        send_email(birth_date, result, email)
    except ValueError:  # Обработка ошибки при вычислении чисел.
        messagebox.showerror("Ошибка", "Ошибка при вычислении чисел. Проверьте введенные данные.")

def send_email(birth_date, result, receiver_email):     # Функция для отправки электронного письма с результатами.
    # Настройки SMTP сервера.
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "yarukguzovaty432@gmail.com"
    password = "kmka xxpy utdt ihfa"
    
    # Формирование письма.
    msg = EmailMessage()
    msg.set_content(result)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = f"Характеристики по дате рождения {birth_date}"
    
    # Отправка письма.
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            messagebox.showinfo("Успех", "Характеристики отправлены на указанную почту!")
    except Exception as e:  # Обработка ошибки при отправке письма.
        messagebox.showerror("Ошибка", f"Не удалось отправить письмо: {str(e)}")

# Создание графического интерфейса.
root = tk.Tk()
root.title("Квадрат Пифагора")

label_name = tk.Label(root, text="Введите имя:")  # Поле для ввода имени.
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

label_date = tk.Label(root, text="Введите дату рождения (дд.мм.гггг):")  # Поле для ввода даты рождения.
label_date.pack()
entry_date = tk.Entry(root)
entry_date.pack()

label_email = tk.Label(root, text="Введите адрес электронной почты:")  # Поле для ввода адреса электронной почты.
label_email.pack()
entry_email = tk.Entry(root)
entry_email.pack()

button = tk.Button(root, text="Рассчитать", command=calculate_pythagoras)  # Кнопка для начала вычислений.
button.pack()

root.mainloop()  # Запуск графического интерфейса.

