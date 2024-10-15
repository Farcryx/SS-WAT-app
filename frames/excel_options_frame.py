import tkinter
import customtkinter as ctk
from tkinter import ttk
from src.logic.finance_logic_excel import read_excel, read_titles, read_pdf, read_column

sheet_names = None
workbook = None
number_of_active_sheet = None


def get_index_of_excel_column(column_str):
    # find first integer from string
    first_int = ''.join(filter(str.isdigit, column_str))
    return int(first_int)


class ExcelOptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, excel_path, pdf_path):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.column_combobox = None
        self.payment_combobox = None
        self.selected_sheet_name = None
        self.selected_album_column = None
        self.selected_payment_column = None
        self.parent = parent
        self.excel_path = excel_path
        self.pdf_path = pdf_path
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Opcje Excel!", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10)
        # Read PDF file
        list_of_albums = read_pdf(self.pdf_path)

        # Read Excel file and get sheet names
        global sheet_names, workbook
        sheet_names, workbook = read_excel(self.excel_path)
        sheet_names_label = ctk.CTkLabel(self, text="Wybierz arkusz:", font=ctk.CTkFont(size=15))

        # Create combobox input from sheet_names
        self.selected_sheet_name = tkinter.StringVar()
        sheet_combobox = ttk.Combobox(self, textvariable=self.selected_sheet_name,
                                      postcommand=self.update_column_combobox, state="readonly")
        sheet_combobox['values'] = sheet_names
        sheet_combobox.bind("<<ComboboxSelected>>", self.update_column_combobox)  # Bind the event to the function
        sheet_combobox.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Wybierz kolumnę z numerem albumu
        column_label = ctk.CTkLabel(self, text="Wybierz kolumnę z numerem albumu:", font=ctk.CTkFont(size=15))
        column_label.grid(row=3, column=0, padx=20, pady=10)

        # Create combobox input for column selection
        self.selected_album_column = tkinter.StringVar()
        self.column_combobox = ttk.Combobox(self, textvariable=self.selected_album_column, state="readonly")
        self.column_combobox.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Wybierz kolumnę z potwierdzeniem dokonanej płatności
        column_payment_label = ctk.CTkLabel(self, text="Wybierz kolumnę z potwierdzeniem dokonanej płatności:",
                                            font=ctk.CTkFont(size=15))
        column_payment_label.grid(row=5, column=0, padx=20, pady=10)

        # Create combobox input for payment column selection
        self.selected_payment_column = tkinter.StringVar()
        self.payment_combobox = ttk.Combobox(self, textvariable=self.selected_payment_column, state="readonly")
        self.payment_combobox.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        # Zatwierdź lub wróć
        submit_button = ctk.CTkButton(self, text="Rozpocznij analizę", command=self.submit_data)
        submit_button.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        back_button = ctk.CTkButton(self, text="Wróć", command=self.go_back)
        back_button.grid(row=8, column=0, padx=20, pady=10, sticky="ew")

    def go_back(self):
        self.grid_forget()

    def update_column_combobox(self, event=None):
        sheet_name = self.selected_sheet_name.get()
        print(sheet_name)
        # find sheet_name in sheet_names and return its position in the list
        if sheet_name:
            global sheet_names, number_of_active_sheet

            sheet_name = sheet_names.index(sheet_name)
            number_of_active_sheet = sheet_name
            print(sheet_name)
            column_titles = read_titles(workbook, sheet_name)
            self.column_combobox['values'] = column_titles
            self.payment_combobox['values'] = column_titles

    def submit_data(self):
        if self.selected_sheet_name.get() and self.selected_album_column.get() and self.selected_payment_column.get():
            # Ukrywamy aktualną ramkę ExcelOptionsFrame, zamiast ją niszczyć
            self.grid_forget()
            print(f"Wybrany arkusz: {self.selected_sheet_name.get()}")
            print(f"Wybrana kolumna z numerem albumu: {self.selected_album_column.get()}")
            print(f"Wybrana kolumna z płatnościami: {self.selected_payment_column.get()}")

            print(f"Numer kolumny Excel: {get_index_of_excel_column(self.selected_album_column.get())}")

            # Get column with album numbers
            album_column_from_excel = read_column(workbook, number_of_active_sheet,
                                                  get_index_of_excel_column(self.selected_album_column.get()))
            print(f"Odczytane komórki z numerami albumów: {album_column_from_excel}")

            # Get column with payment confirmation
            payment_column_from_excel = read_column(workbook, number_of_active_sheet,
                                                    get_index_of_excel_column(self.selected_payment_column.get()))
            print(f"Odczytane komórki z potwierdzeniem płatności: {payment_column_from_excel}")

        else:
            print("Nie wybrano arkusza lub kolumny!")
