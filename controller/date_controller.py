from datetime import datetime, date


class DateController(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    @staticmethod
    def get_date():
        while True:
            birth_date = input('enter student date of birth dd/mm/yyyy : ')
            x = datetime.strptime(birth_date, "%d/%m/%Y")
            return date.strftime(x, "%Y/%m/%d")
