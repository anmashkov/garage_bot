import tkinter as tk
from tkinter import messagebox


class Garage:
    def __init__(self):
        self.fields = {}
        self.window = tk.Tk()
        self.window.geometry('400x300')
        self.window.title('Калькулятор индекса массы тела (ИМТ)')
        self.frame = self.get_frame()

        self.crete_fields()
        self.set_frame_pack()

        print(self.fields)

    def run(self):
        self.window.mainloop()

    def add_field(self, key, field):
        self.fields[key] = field

    def get_field_value(self, key):
        return self.fields[key]['entry'].get()

    def crete_fields(self):
        self.add_field('height', self.create_field("Введите свой рост (в см)  ", row=3, column=1))
        self.add_field('weight', self.create_field("Введите свой вес (в кг)  ", row=4, column=1))
        self.add_button('Рассчитать ИМТ', self.calculate_bmi, row=5, column=2)

    def create_field(self, text, row, column, inline=True):
        lb = self.get_label(text, row, column)
        en = self.get_entry(row, column + int(inline))

        return {
            'label': lb,
            'entry': en
        }

    def get_frame(self):
        return tk.Frame(
            self.window,
            padx=10,
            pady=10
        )

    def get_label(self, text, row, column):
        lb = tk.Label(
            self.frame,
            text=text
        )
        lb.grid(row=row, column=column)

        return lb

    def get_entry(self, row, column):
        en = tk.Entry(
            self.frame,
        )
        en.grid(row=row, column=column)

        return en

    def set_frame_pack(self):
        self.frame.pack(expand=True)

    def add_button(self, text, command, row, column):
        btn = tk.Button(
            self.frame,
            text=text,
            command=command
        )
        btn.grid(row=row, column=column)

        return btn

    def calculate_bmi(self):
        kg = int(self.get_field_value('weight'))
        m = int(self.get_field_value('height')) / 100

        bmi = kg / (m * m)
        bmi = round(bmi, 1)

        if bmi < 18.5:
            messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует недостаточному весу')
        elif (bmi > 18.5) and (bmi < 24.9):
            messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует нормальному весу')
        elif (bmi > 24.9) and (bmi < 29.9):
            messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует избыточному весу')
        else:
            messagebox.showinfo('bmi-pythonguides', f'ИМТ = {bmi} соответствует ожирению')


