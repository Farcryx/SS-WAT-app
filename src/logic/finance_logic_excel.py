import openpyxl
from pypdf import PdfReader

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
    print(f"Lista albumów z pdf: {list_of_albums_from_pdf}")
    return list_of_albums_from_pdf


def run_logic(pdf_path, excel_path):
    # later implementation
    pass
