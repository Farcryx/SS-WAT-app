import tkinter
import customtkinter as ctk
from src.logic.finance_logic_excel import read_titles


class ExcelColumnFrame(ctk.CTkFrame):
    def __init__(self, parent, excel_path, sheet_name_number, workbook):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.selected_column = None
        self.parent = parent
        self.excel_path = excel_path
        self.sheet_name = sheet_name_number
        self.workbook = workbook
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    # TODO: Zamienić formę wyboru kolumny na combobox, w celu umożliwienia wyboru wielu kolumn
    # TODO: Umożliwić użytkownikowi wybór kolumny z numerem albumu oraz kolumny z informacją czy zapłacone
    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Kolumny Excel!", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10)

        # Wybierz kolumnę z numerem albumu
        column_label = ctk.CTkLabel(self, text="Wybierz kolumnę z numerem albumu:", font=ctk.CTkFont(size=15))
        column_label.grid(row=1, column=0, padx=20, pady=10)

        # Read Excel column titles
        column_titles = read_titles(self.workbook, self.sheet_name)
        print(column_titles)

        # Create radio input from column titles
        n = 0
        self.selected_column = tkinter.IntVar()

        for column_nr, column_title in column_titles:
            column_button = ctk.CTkRadioButton(self, text=column_title, variable=self.selected_column, value=column_nr)
            column_button.grid(row=2 + n, column=0, padx=20, pady=10, sticky="ew")
            if n == 0:
                self.selected_column.set(column_nr)
            n += 1

        submit_button = ctk.CTkButton(self, text="Zatwierdź",
                                      # command=self.get_column(self.selected_column)
                                      )
        submit_button.grid(row=10, column=0, padx=20, pady=10, sticky="ew")
        back_button = ctk.CTkButton(self, text="Wróć",
                                    # command=self.go_back
                                    )
        back_button.grid(row=11, column=0, padx=20, pady=10, sticky="ew")
