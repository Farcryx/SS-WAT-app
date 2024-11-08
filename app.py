import os
import customtkinter
from tkinter import filedialog
from PIL import Image

from frames.app_info_frame import AppInfoFrame
from frames.home_frame import HomeFrame
from frames.other_frame import OtherPage
from frames.payments_frame import PaymentsFrame

from src.logic.finance_logic_excel import read_excel

pdf_path = ''
excel_path = ''

customtkinter.set_default_color_theme('dark-blue')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.navigation_frame_label = None
        self.logo_image = None
        self.navigation_frame = None
        self.forward_button = None
        self.back_button = None
        self.navigation_panel = None
        self.title("SS WAT")
        self.geometry("700x450")
        self.configure_grid()
        self.load_images()
        self.create_navigation_panel()
        self.create_navigation_frame()
        self.create_frames()
        self.select_frame_by_name("Strona główna")

    def configure_grid(self):
        self.grid_rowconfigure(0, weight=0)  # Navigation panel row
        self.grid_rowconfigure(1, weight=1)  # Main content row
        self.grid_columnconfigure(1, weight=1)

    def load_images(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "src")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))

    def create_navigation_panel(self):
        self.navigation_panel = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_panel.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.navigation_panel.grid_columnconfigure(0, weight=1)
        self.navigation_panel.grid_columnconfigure(1, weight=1)
        self.navigation_panel.grid_columnconfigure(2, weight=1)

        self.back_button = customtkinter.CTkButton(self.navigation_panel, text="<", command=self.go_back)
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.forward_button = customtkinter.CTkButton(self.navigation_panel, text=">", command=self.go_forward)
        self.forward_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    def create_navigation_frame(self):
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=1, column=0, sticky="nsew")
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
            "Strona główna": HomeFrame(self),
            "Płatności": PaymentsFrame(self),
            "O aplikacji": AppInfoFrame(self),
            "Inne": OtherPage(self),
        }

    def select_frame_by_name(self, name):
        for frame_name, frame in self.frames.items():
            frame.grid_forget() if frame_name != name else frame.grid(row=1, column=1, sticky="nsew")

    def home_button_event(self):
        self.select_frame_by_name("Strona główna")

    def finance_button_event(self):
        self.select_frame_by_name("Płatności")

    def other_button_event(self):
        self.select_frame_by_name("Inne")

    def app_info_event(self):
        self.select_frame_by_name("O aplikacji")

    def go_back(self):
        # Implement the logic for going back
        pass

    def go_forward(self):
        # Implement the logic for going forward
        pass

    def select_pdf_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki PDF", "*.pdf")])
        if file_path:
            self.pdf_file_label.configure(text=os.path.basename(file_path))
            print(f"Selected PDF file: {file_path}")
            global pdf_path
            pdf_path = file_path

    def select_xlsx_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki Excel", "*.xlsx")])
        if file_path:
            self.xlsx_file_label.configure(text=os.path.basename(file_path))
            input_dialog = customtkinter.CTkInputDialog(

            )
            print(f"Selected XLSX file: {file_path}")
            global excel_path
            excel_path = file_path

    def excel_options(self):
        pass
        # frame.grid_forget()

    def input_dialog(self):
        pass
        dialog = customtkinter.CTkInputDialog(text="Wybierz tablicę")
        radio = customtkinter.CTkRadioButton()

    def submit_data(self):
        print(f"Selected PDF file: {self.pdf_file_label.cget('text')}")
        print(f"Selected XLSX file: {self.xlsx_file_label.cget('text')}")
        sheetnames = read_excel(excel_path)
        print(sheetnames)
        # radio = customtkinter.CTkRadioButton(sheetnames)
        # app.create_excel_options()

        # run_logic(pdf_path, excel_path)

        # TODO: Do przeniesienia do innego ekranu
        # print(f"Nazwa kolumny z potwierdzeniem: {self.column_name_entry.get()}")
        # print(f"Nazwa kolumny z numerem albumu: {self.column_nrlabel.get()}")


if __name__ == "__main__":
    app = App()
    app.mainloop()