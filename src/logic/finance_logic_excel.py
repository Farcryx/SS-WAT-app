import openpyxl
from pypdf import PdfReader

# Define values for reading excel file
min_row = 1
max_row = 10
min_col = 1
max_col = 20

tytuly_kolumn = []
lista_albumow = []
lista_czy_zaplacone = []
pdf_lista_albumow = []
wb = None
sheet_names = None


def read_titles(workbook, active_sheet_number):
    # Read column titles
    global sheet_names
    wb = workbook
    active_sheet = wb[sheet_names[active_sheet_number]]
    for col in range(min_col, max_col):
        if active_sheet.cell(row=min_row, column=col).value is not None:
            tytuly_kolumn.append([col, active_sheet.cell(row=min_row, column=col).value])
            print(active_sheet.cell(row=min_row, column=col).value)
    return tytuly_kolumn


def read_column(active_sheet, column_nr):
    row = active_sheet.max_row
    for row in range(min_row + 1, row):
        if active_sheet.cell(row=row, column=column_nr).value:
            lista_albumow.append([row, active_sheet.cell(row=row, column=7).value])


def read_excel(file_path):
    try:
        global wb
        wb = openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
        return

    global sheet_names
    sheet_names = wb.sheetnames
    print(sheet_names)
    return sheet_names, wb

    # n = 0
    # print(sheet_names[n])
    # ws = wb[sheet_names[n]]
    # row = ws.max_row
    # column = ws.max_column

    # read_titles(ws)

    # # Read 7th column
    # for row in range(min_row + 1, row):
    #     if ws.cell(row=row, column=7).value:
    #         lista_albumow.append([row, ws.cell(row=row, column=7).value])
    #
    # # Read 8th column
    # for row in range(min_row + 1, row):
    #     if ws.cell(row=row, column=7).value:
    #         lista_czy_zaplacone.append([row, ws.cell(row=row, column=8).value])

    # print(tytuly_kolumn)
    # print(lista_albumow)
    # print(lista_czy_zaplacone)


def read_pdf(file_path):
    reader = PdfReader(file_path)
    print(len(reader.pages))
    tresc_pdf = ""
    for i in range(len(reader.pages)):
        tresc_pdf += reader.pages[i].extract_text()

    pdf_lista_albumow.extend(x for x in tresc_pdf.split('\n') if x.isdigit() and len(x) == 5)
    print(pdf_lista_albumow)


def run_logic(pdf_path, excel_path):
    print("Running logic...")
    print(f"Ścieżka do pdf: {pdf_path}")
    print(f"Ścieżka do excela: {excel_path}")
    read_excel(excel_path)
    read_pdf(pdf_path)
    # read_pdf(r'/Users/lukaszsokol/Desktop/Praca/WAT - SS/Bal Studenta/FinalnaRealizacjaPlatnosci/Wpłaty 19.03.24.pdf')
    # read_excel(r'/Users/lukaszsokol/Desktop/Praca/WAT - SS/Bal Studenta/FinalnaRealizacjaPlatnosci/bal-kopia.xlsx')


if __name__ == '__main__':
    run_logic()
