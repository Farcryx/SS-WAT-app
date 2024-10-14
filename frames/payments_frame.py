import os
import customtkinter as ctk
from tkinter import filedialog

from frames.excel_options_frame import ExcelOptionsFrame


class PaymentsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.create_widgets()
        self.pdf_path = None
        self.excel_path = None

    def create_widgets(self):
        payments_title = ctk.CTkLabel(self, text="Weryfikacja płatności",
                                      font=ctk.CTkFont(size=20, weight="bold"))
        payments_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        pdf_file_button = ctk.CTkButton(self, text="Wybierz plik PDF", command=self.select_pdf_file)
        pdf_file_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        # Upewnij się, że przypisujesz do self
        self.pdf_file_label = ctk.CTkLabel(self, text=" ")
        self.pdf_file_label.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        xlsx_file_button = ctk.CTkButton(self, text="Wybierz plik XLSX", command=self.select_xlsx_file)
        xlsx_file_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        # Upewnij się, że przypisujesz do self
        self.xlsx_file_label = ctk.CTkLabel(self, text=" ")
        self.xlsx_file_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        submit_button = ctk.CTkButton(self, text="Zatwierdź", command=self.submit_data)
        submit_button.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

    def select_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki PDF", "*.pdf")])
        if file_path:
            self.pdf_file_label.configure(text=os.path.basename(file_path))
            print(f"Selected PDF file: {file_path}")
            self.pdf_path = file_path

    def select_xlsx_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki Excel", "*.xlsx")])
        if file_path:
            self.xlsx_file_label.configure(text=os.path.basename(file_path))
            print(f"Selected XLSX file: {file_path}")
            self.excel_path = file_path

    def submit_data(self):
        if self.excel_path:
            # Ukrywamy aktualną ramkę PaymentsFrame, zamiast ją niszczyć
            self.grid_forget()

            # Tworzymy nową ramkę ExcelOptionsFrame w tym samym miejscu
            ExcelOptionsFrame(self.parent, self.excel_path).grid(row=0, column=1, sticky="nsew")
        else:
            print("Proszę wybrać plik Excel przed przejściem dalej.")
