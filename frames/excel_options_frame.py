import tkinter
import customtkinter as ctk
import datetime
from tkinter import ttk
from src.logic.finance_logic_excel import read_excel, read_titles, read_document, read_column, analyze_data, \
    write_to_log_file

sheet_names = None
workbook = None
number_of_active_sheet = None

def get_index_of_excel_column(column_str):
    first_int = ''.join(filter(str.isdigit, column_str))
    return int(first_int)

class ExcelOptionsFrame(ctk.CTkFrame):
    # pdf_paths now gets a list of document paths instead of a single file
    def __init__(self, parent, excel_path, pdf_paths, log_file):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.column_combobox = None
        self.payment_combobox = None
        self.selected_sheet_name = None
        self.selected_album_column = None
        self.selected_payment_column = None
        self.parent = parent
        self.excel_path = excel_path
        self.pdf_paths = pdf_paths
        self.log_file = log_file
        self.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self, text="Opcje Excel!", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10)
        # Read Excel file and get sheet names
        global sheet_names, workbook
        sheet_names, workbook = read_excel(self.excel_path)
        sheet_names_label = ctk.CTkLabel(self, text="Wybierz arkusz:", font=ctk.CTkFont(size=15))
        sheet_names_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.selected_sheet_name = tkinter.StringVar()
        sheet_combobox = ttk.Combobox(self, textvariable=self.selected_sheet_name,
                                      postcommand=self.update_column_combobox, state="readonly")
        sheet_combobox['values'] = sheet_names
        sheet_combobox.bind("<<ComboboxSelected>>", self.update_column_combobox)
        sheet_combobox.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        column_label = ctk.CTkLabel(self, text="Wybierz kolumnę z numerem albumu:", font=ctk.CTkFont(size=15))
        column_label.grid(row=3, column=0, padx=20, pady=10)
        self.selected_album_column = tkinter.StringVar()
        self.column_combobox = ttk.Combobox(self, textvariable=self.selected_album_column, state="readonly")
        self.column_combobox.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        column_payment_label = ctk.CTkLabel(self, text="Wybierz kolumnę z potwierdzeniem płatności:",
                                            font=ctk.CTkFont(size=15))
        column_payment_label.grid(row=5, column=0, padx=20, pady=10)
        self.selected_payment_column = tkinter.StringVar()
        self.payment_combobox = ttk.Combobox(self, textvariable=self.selected_payment_column, state="readonly")
        self.payment_combobox.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        submit_button = ctk.CTkButton(self, text="Rozpocznij analizę", command=self.submit_data)
        submit_button.grid(row=7, column=0, padx=20, pady=10, sticky="ew")
        back_button = ctk.CTkButton(self, text="Wróć", command=self.go_back)
        back_button.grid(row=8, column=0, padx=20, pady=10, sticky="ew")
        write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Załadowano GUI opcji Excel\n")

    def go_back(self):
        self.grid_forget()

    def update_column_combobox(self, event=None):
        sheet_name = self.selected_sheet_name.get()
        write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Wybrano arkusz: {sheet_name}\n")
        if sheet_name:
            global sheet_names, number_of_active_sheet
            number_of_active_sheet = sheet_names.index(sheet_name)
            column_titles = read_titles(workbook, number_of_active_sheet)
            self.column_combobox['values'] = column_titles
            self.payment_combobox['values'] = column_titles
            write_to_log_file(self.log_file,
                              f"{datetime.datetime.now()} - Załadowano tytuły kolumn z arkusza: {column_titles}\n")

    def submit_data(self):
        if self.selected_sheet_name.get() and self.selected_album_column.get() and self.selected_payment_column.get():
            write_to_log_file(self.log_file,
                              f"{datetime.datetime.now()} - Wybrano kolumnę z albumami {self.selected_album_column.get()} oraz z potwierdzeniem płatności {self.selected_payment_column.get()}\n")
            self.grid_forget()
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Przejście do analizy danych\n")
            # For each selected document analyze data one by one
            for document_file in self.pdf_paths:
                analyze_data(workbook,
                             self.excel_path,
                             document_file,
                             number_of_active_sheet,
                             get_index_of_excel_column(self.selected_album_column.get()),
                             get_index_of_excel_column(self.selected_payment_column.get()),
                             self.log_file)
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Zakończono analizę danych\n")
            write_to_log_file(self.log_file)
        else:
            print("Nie wybrano arkusza lub kolumny!")