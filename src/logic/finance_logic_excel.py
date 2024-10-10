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


def read_excel(file_path):
    try:
        wb = openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
        return
    print(wb.sheetnames)
    n = 0
    sheetnames = wb.sheetnames
    print(sheetnames[n])
    ws = wb[sheetnames[n]]
    row = ws.max_row
    column = ws.max_column

    # Read column titles
    for col in range(min_col, max_col):
        if ws.cell(row=min_row, column=col).value is not None:
            tytuly_kolumn.append([col, ws.cell(row=min_row, column=col).value])

    # Read 7th column
    for row in range(min_row + 1, row):
        if ws.cell(row=row, column=7).value:
            lista_albumow.append([row, ws.cell(row=row, column=7).value])

    # Read 8th column
    for row in range(min_row + 1, row):
        if ws.cell(row=row, column=7).value:
            lista_czy_zaplacone.append([row, ws.cell(row=row, column=8).value])

    print(tytuly_kolumn)
    print(lista_albumow)
    print(lista_czy_zaplacone)


def read_pdf(file_path):
    reader = PdfReader(file_path)
    # printing number of pages in pdf file
    print(len(reader.pages))
    tresc_pdf = ""
    for i in range(len(reader.pages)):
        # print(reader.pages[i].extract_text())
        tresc_pdf += reader.pages[i].extract_text()

    pdf_lista_albumow.extend(x for x in tresc_pdf.split('\n') if x.isdigit() and len(x) == 5)
    print(pdf_lista_albumow)


def run_logic():
    read_pdf(r'/Users/lukaszsokol/Desktop/Praca/WAT - SS/Bal Studenta/FinalnaRealizacjaPlatnosci/Wpłaty 19.03.24.pdf')
    read_excel(r'/Users/lukaszsokol/Desktop/Praca/WAT - SS/Bal Studenta/FinalnaRealizacjaPlatnosci/bal-kopia.xlsx')


if __name__ == '__main__':
    run_logic()
