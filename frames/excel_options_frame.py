import tkinter
import customtkinter as ctk

from frames.excel_columns_frame import ExcelColumnFrame
# from frames.payments_frame import PaymentsFrame
from src.logic.finance_logic_excel import read_excel

sheet_names = None
workbook = None


class ExcelOptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, excel_path):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.selected_sheet_name = None
        self.parent = parent
        self.excel_path = excel_path
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Opcje Excel!", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10)

        global sheet_names, workbook
        sheet_names, workbook = read_excel(self.excel_path)
        sheet_names_label = ctk.CTkLabel(self, text="Wybierz arkusz:", font=ctk.CTkFont(size=15))

        # Create a variable to hold the selected sheet_name
        self.selected_sheet_name = tkinter.IntVar()

        # Create radio input from sheet_names
        for count, sheet_name in enumerate(sheet_names):
            sheet_button = ctk.CTkRadioButton(self, text=sheet_name, variable=self.selected_sheet_name, value=count)
            sheet_button.grid(row=2 + count, column=0, padx=20, pady=10, sticky="ew")
            if count == 0:  # Ustawiamy domyślnie pierwszy radio button jako wybrany
                self.selected_sheet_name.set(count)

        submit_button = ctk.CTkButton(self, text="Zatwierdź", command=self.submit_data)
        submit_button.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        back_button = ctk.CTkButton(self, text="Wróć", command=self.go_back)
        back_button.grid(row=8, column=0, padx=20, pady=10, sticky="ew")

    def go_back(self):
        self.grid_forget()

    def submit_data(self):
        if self.selected_sheet_name:
            # Ukrywamy aktualną ramkę ExcelOptionsFrame, zamiast ją niszczyć
            self.grid_forget()
            print(sheet_names[self.selected_sheet_name.get()])

            # Tworzymy nową ramkę PaymentsFrame w tym samym miejscu
            ExcelColumnFrame(self.parent, self.excel_path, self.selected_sheet_name.get(), workbook).grid(row=0,
                                                                                                          column=1,
                                                                                                          sticky="nsew")
        else:
            print("Nie wybrano arkusza!")
