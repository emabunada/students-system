import mariadb


class DbController(object):
    conn = mariadb.connect(user="root", password="12341234", host="localhost", database="students_db")

    cur = conn.cursor()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance




