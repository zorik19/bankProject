from enum import Enum

PROJECT_NAME = 'lead_service'


class LeadSourceType(Enum):
    """
    Enum for LeadSource models.
    As it rare changes  - we can use it as enum
    """
    MANUAL: int = 1  # Вручную
    XLSX: int = 2  # Данные внесены через xlsx
    OUTER: int = 3  # По внешней ссылке
    FORM: int = 4  # Клиент заполнил форму

    def __str__(self):
        return str(self.value)


FORMAT_TO_MIME_TYPE = {
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'csv': 'text/csv'
    }

LEAD_TYPE_TO_ID = {
    'победитель': 1,
    'постоянный клиент': 2,
    'участник': 3,
    'агент': 4,
    'аналитика': 5,
    }

BULK_INSERT_LIMIT = 100


class LeadStatusEnum(Enum):
    """
    Enum for LeadStatus models.
    As it rare changes  - we can use it as enum
    """
    NOT_PHONED: int = 1
    WAIT_FOR_PAY: int = 2
    CHANGE_TIME: int = 3
    DENIAL: int = 4
    PRODUCTION: int = 5

    def __str__(self):
        return str(self.value)
