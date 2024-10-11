import os
import customtkinter
from tkinter import filedialog
from PIL import Image
# import sys
# sys.path.insert(1, 'src/logic/finance_logic_excel.py')
# import file
from src.logic.finance_logic_excel import run_logic


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("SS WAT")
        self.geometry("700x450")
        self.configure_grid()
        self.load_images()
        self.create_navigation_frame()
        self.create_frames()
        self.select_frame_by_name("Strona główna")

    def configure_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def load_images(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "src")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))

    def create_navigation_frame(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  SS WAT",
                                                             image=self.logo_image,
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Buttons in the navigation menu
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        buttons_data = [
            ("Strona główna", self.home_button_event),
            ("Płatności", self.finance_button_event),
            ("Inne", self.other_button_event),
            ("O aplikacji", self.app_info_event)
        ]
        for i, (text, command) in enumerate(buttons_data):
            button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                             text=text, fg_color="transparent", text_color=("gray10", "gray90"),
                                             hover_color=("gray70", "gray30"), command=command)
            if i == 3:
                button.grid(row=i + 1, column=0, sticky="s")
            else:
                button.grid(row=i + 1, column=0, sticky="ew")

    def create_frames(self):
        self.frames = {
            "Strona główna": self.create_home_frame(),
            "Płatności": self.create_payments_frame(),
            "O aplikacji": self.create_app_info_frame(),
            "Inne": self.create_other_frame(),
        }

    def create_home_frame(self):
        home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        home_frame.grid_columnconfigure(0, weight=1)
        home_frame_title = customtkinter.CTkLabel(home_frame, text="Witaj w aplikacji SS WAT!",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        home_frame_title.grid(row=0, column=0, padx=20, pady=10)
        return home_frame

    def create_payments_frame(self):
        payments_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        payments_frame.grid_columnconfigure(0, weight=1)

        payments_title = customtkinter.CTkLabel(payments_frame, text="Weryfikacja płatności",
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        payments_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.pdf_file_button = customtkinter.CTkButton(payments_frame, text="Wybierz plik PDF",
                                                       command=self.select_pdf_file)
        self.pdf_file_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.pdf_file_label = customtkinter.CTkLabel(payments_frame, text="")
        self.pdf_file_label.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.csv_file_button = customtkinter.CTkButton(payments_frame, text="Wybierz plik CSV",
                                                       command=self.select_csv_file)
        self.csv_file_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.csv_file_label = customtkinter.CTkLabel(payments_frame, text="")
        self.csv_file_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.column_name_label = customtkinter.CTkLabel(payments_frame,
                                                        text="Nazwa kolumny z potwierdzeniem weryfikacji:")
        self.column_name_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.column_name_entry = customtkinter.CTkEntry(payments_frame)
        self.column_name_entry.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        # Pole do wprowadzenia kolumny z nr albumu
        self.column_nrlabel = customtkinter.CTkLabel(payments_frame,
                                                     text="Nazwa kolumny z numerem albumu:")
        self.column_nrlabel.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.column_nrlabel = customtkinter.CTkEntry(payments_frame)
        self.column_nrlabel.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        self.submit_button = customtkinter.CTkButton(payments_frame, text="Zatwierdź", command=self.submit_data)
        self.submit_button.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        return payments_frame

    def create_app_info_frame(self):
        app_info_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        app_info_frame.grid_columnconfigure(0, weight=1)
        app_info_title = customtkinter.CTkLabel(app_info_frame, text="O aplikacji",
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        app_info_title.grid(row=0, column=0, padx=20, pady=10)
        return app_info_frame

    def create_other_frame(self):
        other_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        other_frame.grid_columnconfigure(0, weight=1)
        other_frame_title = customtkinter.CTkLabel(other_frame, text="Inne",
                                                   font=customtkinter.CTkFont(size=20, weight="bold"))
        other_frame_title.grid(row=0, column=0, padx=20, pady=10)
        return other_frame

    def select_frame_by_name(self, name):
        for frame_name, frame in self.frames.items():
            frame.grid_forget() if frame_name != name else frame.grid(row=0, column=1, sticky="nsew")

    def home_button_event(self):
        self.select_frame_by_name("Strona główna")

    def finance_button_event(self):
        self.select_frame_by_name("Płatności")

    def other_button_event(self):
        self.select_frame_by_name("Inne")

    def app_info_event(self):
        self.select_frame_by_name("O aplikacji")

    def select_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki PDF", "*.pdf")])
        if file_path:
            self.pdf_file_label.configure(text=os.path.basename(file_path))
            print(f"Selected PDF file: {file_path}")

    def select_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki CSV", "*.csv")])
        if file_path:
            self.csv_file_label.configure(text=os.path.basename(file_path))
            print(f"Selected CSV file: {file_path}")

    def submit_data(self):
        print(f"Selected PDF file: {self.pdf_file_label.cget('text')}")
        print(f"Selected CSV file: {self.csv_file_label.cget('text')}")
        print(f"Nazwa kolumny z potwierdzeniem: {self.column_name_entry.get()}")
        print(f"Nazwa kolumny z numerem albumu: {self.column_nrlabel.get()}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
