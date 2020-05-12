from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Border, Font, Side
from openpyxl.styles.borders import BORDER_THIN
from openpyxl.utils import get_column_letter

HEADER_FIELDS = [
    '№ Аукциона',
    'Дата',
    'Сумма БГ',
    'Название',
    'ИНН',
    'E-mail',
    'Конт. Лицо',
    'Описание',
    'Телефон',
    'ФЗ',
    'Регион',
    'Наименование базы',
    ]
HEADER_FONT_SIZE = 12
HEADER_FONT = Font(name='Arial', size=HEADER_FONT_SIZE, bold=True)
FIRST_COLUMN = 1
ADJUST_CONST = 2  # experimental(could be changed) additional val to see the whole text in the cell
ADJUST_COEFFICIENT = HEADER_FONT_SIZE / 10

HEADER_BORDER = Border(left=Side(border_style=BORDER_THIN,
                                 color='FF000000'),
                       right=Side(border_style=BORDER_THIN,
                                  color='FF000000'),
                       top=Side(border_style=BORDER_THIN,
                                color='FF000000'),
                       bottom=Side(border_style=BORDER_THIN,
                                   color='FF000000'), )


def parse_xlsx(skip_header=True):
    ...


def generate_xlsx(name: str = 'example.xlsx') -> BytesIO:
    wb = Workbook()
    ws = wb.active
    for i, val in enumerate(HEADER_FIELDS):
        i += FIRST_COLUMN
        col_letter = get_column_letter(i)
        cell_name = col_letter + str(FIRST_COLUMN)

        ws[cell_name].font = HEADER_FONT  # can use ws(row=1, column=i)
        ws[cell_name].border = HEADER_BORDER
        ws.column_dimensions[col_letter].width = (len(val) + ADJUST_CONST) * ADJUST_COEFFICIENT

        ws[cell_name] = val

    output = BytesIO()
    wb.save(output)
    output.name = name
    return output


if __name__ == '__main__':
    name = 'test.xlsx'
    generate_xlsx(name)
