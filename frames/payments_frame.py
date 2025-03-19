import os
import customtkinter as ctk
import tkinter
import datetime

from frames.excel_options_frame import ExcelOptionsFrame
from src.logic.finance_logic_excel import create_log_file, write_to_log_file
from tkinter import filedialog

class PaymentsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.create_widgets()
        self.pdf_paths = []   # <-- Changed from single pdf_path to list
        self.excel_path = None
        self.log_file = create_log_file()
    
    def print_dependencies(self):
        # Print the dependencies with the version numbers
        print("Dependencies:")
        print(f"customtkinter: {ctk.__version__}")
        print(f"Python: {os.sys.version}")
        print(f"Tkinter: {tkinter.TkVersion}")


    def create_widgets(self):
        payments_title = ctk.CTkLabel(self, text="Weryfikacja płatności",
                                      font=ctk.CTkFont(size=20, weight="bold"))
        payments_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        pdf_file_button = ctk.CTkButton(self, text="Wybierz plik PDF/DOCX", command=self.select_pdf_file)
        pdf_file_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.pdf_file_label = ctk.CTkLabel(self, text="Nie wybrano pliku", anchor="w")
        self.pdf_file_label.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        xlsx_file_button = ctk.CTkButton(self, text="Wybierz plik XLSX", command=self.select_xlsx_file)
        xlsx_file_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.xlsx_file_label = ctk.CTkLabel(self, text="Nie wybrano pliku", anchor="w")
        self.xlsx_file_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        submit_button = ctk.CTkButton(self, text="Zatwierdź", command=self.submit_data)
        submit_button.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def select_pdf_file(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf"), ("DOCX Files", "*.docx")])
        if file_paths:
            self.pdf_file_label.configure(text=f"Pomyślnie wybrano {len(file_paths)} plików")
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Wybrano pliki: {file_paths}\n")
            self.pdf_paths = list(file_paths)

    def select_xlsx_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki Excel", "*.xlsx")])
        if file_path:
            self.xlsx_file_label.configure(text="Pomyślnie wybrano plik XLSX")
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Wybrano plik XLSX: {file_path}\n")
            self.excel_path = file_path

    def submit_data(self):
        self.print_dependencies()
        if self.excel_path:
            # Ukrywamy aktualną ramkę PaymentsFrame, zamiast ją niszczyć
            self.grid_forget()
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Przejście do opcji Excel\n")
            # Przekazujemy listę wybranych plików do opcji Excel
            ExcelOptionsFrame(self.parent, self.excel_path, self.pdf_paths, self.log_file).grid(row=0, column=1, sticky="nsew")
        else:
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Nie wybrano pliku Excel\n")
            print("Proszę wybrać plik Excel przed przejściem dalej.")