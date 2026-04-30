import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Имя файла для сохранения данных
DATA_FILE = "expenses.json"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - Трекер расходов")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        self.expenses = []
        self.load_data()

        self.create_widgets()
        self.refresh_table()

    # ------------------- Работа с JSON -------------------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.expenses = json.load(f)
            except:
                self.expenses = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    # ------------------- GUI элементы -------------------
    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавить расход", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Поле Сумма
        ttk.Label(input_frame, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Поле Категория (выпадающий список)
        ttk.Label(input_frame, text="Категория:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, 
                                           values=["Еда", "Транспорт", "Развлечения", "Здоровье", "Жильё", "Другое"], 
                                           width=15)
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)
        self.category_combo.current(0)

        # Поле Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Кнопка Добавить
        self.add_btn = ttk.Button(input_frame, text="Добавить расход", command=self.add_expense)
        self.add_btn.grid(row=0, column=6, padx=10, pady=5)

        # Рамка для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_category_var = tk.StringVar(value="Все")
        self.filter_category_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var,
                                                  values=["Все", "Еда", "Транспорт", "Развлечения", "Здоровье", "Жильё", "Другое"],
                                                  width=15)
        self.filter_category_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Дата от (ГГГГ-ММ-ДД):").grid(row=0, column=2, padx=5, pady=5)
        self.date_from_entry = ttk.Entry(filter_frame, width=12)
        self.date_from_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(filter_frame, text="Дата до (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5, pady=5)
        self.date_to_entry = ttk.Entry(filter_frame, width=12)
        self.date_to_entry.grid(row=0, column=5, padx=5, pady=5)

        self.filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.refresh_table)
        self.filter_btn.grid(row=0, column=6, padx=10, pady=5)

        self.reset_filter_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filters)
        self.reset_filter_btn.grid(row=0, column=7, padx=5, pady=5)

        # Рамка для суммы за период
        summary_frame = ttk.LabelFrame(self.root, text="Итоги", padding=10)
        summary_frame.pack(fill="x", padx=10, pady=5)

        self.summary_label = ttk.Label(summary_frame, text="Сумма за выбранный период: 0.00", font=("Arial", 12, "bold"))
        self.summary_label.pack()

        # Таблица расходов
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "Дата", "Категория", "Сумма")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Сумма", text="Сумма (₽)")
        
        self.tree.column("id", width=50)
        self.tree.column("Дата", width=120)
        self.tree.column("Категория", width=120)
        self.tree.column("Сумма", width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления записями
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)

        self.delete_btn = ttk.Button(control_frame, text="Удалить выбранную запись", command=self.delete_expense)
        self.delete_btn.pack(side="left", padx=5)

        self.edit_btn = ttk.Button(control_frame, text="Редактировать выбранную запись", command=self.edit_expense)
        self.edit_btn.pack(side="left", padx=5)

    # ------------------- Функции валидации -------------------
    def validate_amount(self, amount_str):
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
            return True, amount
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректная сумма: {e}")
            return False, None

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, date_str
        except:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return False, None

    # ------------------- CRUD операции -------------------
    def add_expense(self):
        amount_str = self.amount_entry.get().strip()
        category = self.category_var.get()
        date_str = self.date_entry.get().strip()

        valid_amount, amount = self.validate_amount(amount_str)
        if not valid_amount:
            return
        
        valid_date, date_val = self.validate_date(date_str)
        if not valid_date:
            return

        # Генерация ID
        new_id = max([e["id"] for e in self.expenses], default=0) + 1
        
        expense = {
            "id": new_id,
            "amount": amount,
            "category": category,
            "date": date_val
        }
        
        self.expenses.append(expense)
        self.save_data()
        self.refresh_table()
        
        # Очистка полей
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        messagebox.showinfo("Успех", "Расход добавлен!")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return
        
        item = self.tree.item(selected[0])
        expense_id = item["values"][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный расход?"):
            self.expenses = [e for e in self.expenses if e["id"] != expense_id]
            self.save_data()
            self.refresh_table()

    def edit_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для редактирования")
            return
        
        item = self.tree.item(selected[0])
        expense_id = item["values"][0]
        
        # Находим расход
        expense = next((e for e in self.expenses if e["id"] == expense_id), None)
        if not expense:
            return
        
        # Окно редактирования
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Редактирование расхода")
        edit_win.geometry("400x250")
        
        ttk.Label(edit_win, text="Сумма:").pack(pady=5)
        amount_edit = ttk.Entry(edit_win)
        amount_edit.insert(0, str(expense["amount"]))
        amount_edit.pack()
        
        ttk.Label(edit_win, text="Категория:").pack(pady=5)
        category_edit = ttk.Combobox(edit_win, values=["Еда", "Транспорт", "Развлечения", "Здоровье", "Жильё", "Другое"])
        category_edit.set(expense["category"])
        category_edit.pack()
        
        ttk.Label(edit_win, text="Дата (ГГГГ-ММ-ДД):").pack(pady=5)
        date_edit = ttk.Entry(edit_win)
        date_edit.insert(0, expense["date"])
        date_edit.pack()
        
        def save_edit():
            valid_amount, new_amount = self.validate_amount(amount_edit.get())
            valid_date, new_date = self.validate_date(date_edit.get())
            
            if valid_amount and valid_date:
                expense["amount"] = new_amount
                expense["category"] = category_edit.get()
                expense["date"] = new_date
                self.save_data()
                self.refresh_table()
                edit_win.destroy()
                messagebox.showinfo("Успех", "Расход обновлён!")
        
        ttk.Button(edit_win, text="Сохранить", command=save_edit).pack(pady=10)

    # ------------------- Фильтрация и отображение -------------------
    def get_filtered_expenses(self):
        filtered = self.expenses.copy()
        
        # Фильтр по категории
        category_filter = self.filter_category_var.get()
        if category_filter != "Все":
            filtered = [e for e in filtered if e["category"] == category_filter]
        
        # Фильтр по дате
        date_from = self.date_from_entry.get().strip()
        date_to = self.date_to_entry.get().strip()
        
        if date_from:
            try:
                from_dt = datetime.strptime(date_from, "%Y-%m-%d")
                filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") >= from_dt]
            except:
                pass
        
        if date_to:
            try:
                to_dt = datetime.strptime(date_to, "%Y-%m-%d")
                filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") <= to_dt]
            except:
                pass
        
        return filtered

    def calculate_sum(self, filtered_expenses):
        total = sum(e["amount"] for e in filtered_expenses)
        self.summary_label.config(text=f"Сумма за выбранный период: {total:.2f} ₽")

    def refresh_table(self):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        filtered = self.get_filtered_expenses()
        
        # Сортируем по дате (новые сверху)
        filtered.sort(key=lambda x: x["date"], reverse=True)
        
        for expense in filtered:
            self.tree.insert("", "end", values=(
                expense["id"],
                expense["date"],
                expense["category"],
                f"{expense['amount']:.2f}"
            ))
        
        self.calculate_sum(filtered)

    def reset_filters(self):
        self.filter_category_var.set("Все")
        self.date_from_entry.delete(0, tk.END)
        self.date_to_entry.delete(0, tk.END)
        self.refresh_table()

# ------------------- Запуск приложения -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()