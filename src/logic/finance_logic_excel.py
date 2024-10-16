import os
import sys

import openpyxl
from pypdf import PdfReader
import datetime

# Define values for reading excel file
min_row = 1
max_row = 10
min_col = 1
max_col = 20
sheet_names = None


def read_titles(workbook, active_sheet_number):
    column_titles = []
    global sheet_names
    active_sheet = workbook[sheet_names[active_sheet_number]]
    for col in range(min_col, max_col):
        if active_sheet.cell(row=min_row, column=col).value is not None:
            column_titles.append([col, active_sheet.cell(row=min_row, column=col).value])
            print(active_sheet.cell(row=min_row, column=col).value)
    return column_titles


def read_column(workbook, active_sheet_number, column_nr):
    list_of_cells_in_column = []
    global sheet_names
    active_sheet = workbook[sheet_names[active_sheet_number]]
    row = active_sheet.max_row
    for row in range(min_row + 1, row):
        if active_sheet.cell(row=row, column=column_nr).value:
            list_of_cells_in_column.append([row, active_sheet.cell(row=row, column=column_nr).value])
    return list_of_cells_in_column


def read_excel(file_path):
    try:
        workbook = openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
        return

    global sheet_names
    sheet_names = workbook.sheetnames
    print(sheet_names)
    return sheet_names, workbook


def read_pdf(file_path):
    reader = PdfReader(file_path)
    print(len(reader.pages))
    pdf_content = ""
    for i in range(len(reader.pages)):
        pdf_content += reader.pages[i].extract_text()
    list_of_albums_from_pdf = []
    list_of_albums_from_pdf.extend(x for x in pdf_content.split('\n') if x.isdigit() and len(x) == 5)
    # print(f"Lista albumów z pdf: {list_of_albums_from_pdf}")
    return list_of_albums_from_pdf


def write_to_log_file(log_file, message):
    try:
        log_file.write(message)
    except Exception as e:
        print(f"Nie udało się zapisać do pliku logów: {e}")
        log_file.close()


def create_log_file():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        try:
            os.makedirs('logs')
        except Exception as e:
            print(f"Nie udało się utworzyć katalogu logów: {e}")
            return None

    # Create log file with current date
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        log_file = open(f"logs/log_{date}.log", "w")
        # Write to log file basic information about the application and system
        write_to_log_file(log_file, f"Logi z aplikacji SS WAT z modułu płatności\n")
        write_to_log_file(log_file, f"Autor aplikacji: Łukasz Sokół\n")
        write_to_log_file(log_file, f"Data utworzenia logów: {date}\n")
        write_to_log_file(log_file, f"System operacyjny: {os.name}\n")
        write_to_log_file(log_file, f"Wersja Pythona: {os.sys.version}\n")
        write_to_log_file(log_file, f"Wersja Openpyxl: {openpyxl.__version__}\n")
        write_to_log_file(log_file, f"Ścieżka do pliku logów: {os.path.abspath(log_file.name)}\n")



        return log_file
    except Exception as e:
        print(f"Nie udało się utworzyć pliku logów: {e}")
        return None


def analyze_data(workbook, excel_path, pdf_path, number_of_active_sheet, index_album_column, index_payment_column,
                 log_file):
    # Get list of albums from PDF
    list_of_albums = read_pdf(pdf_path)
    print(f"Znaleziona liczba albumów w pliku PDF {len(list_of_albums)}")
    write_to_log_file(log_file,
                      f"{datetime.datetime.now()} - Znaleziona liczba albumów w pliku PDF {len(list_of_albums)}\n")
    write_to_log_file(log_file, f"{datetime.datetime.now()} - Znalezione albumy w pliku PDF: {list_of_albums}\n")

    # Get column with album numbers
    album_column_from_excel = read_column(workbook, number_of_active_sheet, index_album_column)
    write_to_log_file(log_file,
                      f"{datetime.datetime.now()} - Znaleziona liczba albumów w pliku Excel {len(album_column_from_excel)}\n")
    write_to_log_file(log_file,
                      f"{datetime.datetime.now()} - Znalezione albumy w pliku Excel: {album_column_from_excel}\n")

    # Find albums from PDF in EXCEL. Found albums are stored in found_albums list, but not found in not_found_albums list.
    found_albums = []
    not_found_albums = []
    for album in list_of_albums:
        found = False
        for row in album_column_from_excel:
            if album in row[1]:
                found_albums.append(album)
                workbook[sheet_names[number_of_active_sheet]].cell(row=row[0],
                                                                   column=index_payment_column).value = "TAK"
                print(f"Wpisano TAK w komórkę {row[0]} w kolumnie {index_payment_column}")
                write_to_log_file(log_file,
                                  f"{datetime.datetime.now()} - Wpisano TAK w komórkę {row[0]} w kolumnie {index_payment_column}\n")
                found = True
                break
        if not found:
            not_found_albums.append(album)
            write_to_log_file(log_file, f"{datetime.datetime.now()} - Nie znaleziono albumu {album} w pliku Excel\n")

    workbook.save(excel_path)
    print(f"Pomyślnie zapisano zmiany w pliku Excel {excel_path}")
    write_to_log_file(log_file, f"{datetime.datetime.now()} - Pomyślnie zapisano zmiany w pliku Excel {excel_path}\n")
    write_to_log_file(log_file, f"Podsumowanie\n")
    write_to_log_file(log_file, f"Znaleziono {len(found_albums)} albumów z pliku PDF w pliku Excel\n")
    write_to_log_file(log_file, f"Nie znaleziono {len(not_found_albums)} albumów z pliku PDF w pliku Excel\n")
    write_to_log_file(log_file, f"Nieznalezione albumy: {not_found_albums}\n")
    # save log file
    log_file.close()
