from controller.db_controller import DbController


class LevelController(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    @staticmethod
    def select_level():
        cur = DbController.cur
        fields = f""" level_name  """
        table_name = f""" level """
        query = f""" select {fields} from {table_name} """
        cur.execute(query)
        data = list(cur)
        print('levels')
        for index in range(0, len(data)):
            print(f"{index + 1}: {data[index][0]}")
        return int(input("select student level: "))