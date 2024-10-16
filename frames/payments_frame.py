import os
import customtkinter as ctk
from tkinter import filedialog
import datetime

from frames.excel_options_frame import ExcelOptionsFrame
from src.logic.finance_logic_excel import create_log_file, write_to_log_file


class PaymentsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.create_widgets()
        self.pdf_path = None
        self.excel_path = None
        self.log_file = create_log_file()

    def create_widgets(self):
        payments_title = ctk.CTkLabel(self, text="Weryfikacja płatności",
                                      font=ctk.CTkFont(size=20, weight="bold"))
        payments_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        pdf_file_button = ctk.CTkButton(self, text="Wybierz plik PDF", command=self.select_pdf_file)
        pdf_file_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        # Upewnij się, że przypisujesz do self
        self.pdf_file_label = ctk.CTkLabel(self, text="Nie wybrano pliku")
        self.pdf_file_label.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        xlsx_file_button = ctk.CTkButton(self, text="Wybierz plik XLSX", command=self.select_xlsx_file)
        xlsx_file_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        # Upewnij się, że przypisujesz do self
        self.xlsx_file_label = ctk.CTkLabel(self, text="Nie wybrano pliku")
        self.xlsx_file_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        submit_button = ctk.CTkButton(self, text="Zatwierdź", command=self.submit_data)
        submit_button.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="ew")


    def select_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki PDF", "*.pdf")])
        if file_path:
            self.pdf_file_label.configure(text="Pomyślnie wybrano plik PDF")
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Wybrano plik PDF: {file_path}\n")
            self.pdf_path = file_path

    def select_xlsx_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki Excel", "*.xlsx")])
        if file_path:
            self.xlsx_file_label.configure(text="Pomyślnie wybrano plik XLSX")
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Wybrano plik XLSX: {file_path}\n")
            self.excel_path = file_path

    def submit_data(self):
        if self.excel_path:
            # Ukrywamy aktualną ramkę PaymentsFrame, zamiast ją niszczyć
            self.grid_forget()
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Przejście do opcji Excel\n")

            # Tworzymy nową ramkę ExcelOptionsFrame w tym samym miejscu
            ExcelOptionsFrame(self.parent, self.excel_path, self.pdf_path, self.log_file).grid(row=0, column=1, sticky="nsew")
        else:
            write_to_log_file(self.log_file, f"{datetime.datetime.now()} - Nie wybrano pliku Excel\n")
            print("Proszę wybrać plik Excel przed przejściem dalej.")
