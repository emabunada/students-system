import datetime

from controller.date_controller import DateController
from controller.db_controller import DbController
from controller.level_controller import LevelController
from models.student import Student


class StudentController(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    @staticmethod
    def get_all_students():
        students = []
        cur = DbController().cur
        fields = f""" s.student_id,s.student_name , s.contact_id,s.address_id,
        s.level_id,s.BOD,c.email,c.mobile_number,a.city """
        query = f""" select {fields} from student as s join address as a join contact as c
         on s.contact_id = c.contact_id and s.address_id = a.address_id """
        DbController().cur.execute(query)
        data = list(cur)
        students = list(map(StudentController.student_from_tuple, data))
        return students

    @staticmethod
    def student_from_tuple(x: tuple):
        student_id = int(x[0])
        name = x[1]
        contact = int(x[2])
        address = int(x[3])
        level = int(x[4])
        bod = datetime.datetime.strftime(x[5], '%d/%m/%Y')
        if len(x) > 6:
            email = x[6]
            phone = x[7]
            city = x[8]
            return Student(student_id, name, contact, address, level, bod, email, phone, city)

        else:
            return Student(student_id, name, contact, address, level, bod)

    @staticmethod
    def get_student_by_id(student_id):
        cur = DbController().cur
        query = f""" select * from student where student_id = {student_id} """
        DbController().cur.execute(query)
        data = list(cur)
        if len(data) > 0:
            student = StudentController.student_from_tuple(data[0])
            return student
        else:
            print("student not found")

    @staticmethod
    def select_address():
        cur = DbController.cur
        fields = f""" address_id , city  """
        table_name = f""" address """
        query = f""" select {fields} from {table_name} """
        cur.execute(query)
        data = list(cur)
        print('addresses')
        for index in range(0, len(data)):
            print(f"{index + 1}: {data[index][0]}\t\t {data[index][1]}")
        x = int(input("select student address: "))
        return data[x - 1][0]

    @staticmethod
    def register_new_student():
        cur = DbController.cur
        print('--------------------------------------------------------------------------------')
        name = input('enter student name  ')
        birth_date = DateController.get_date()
        level = LevelController.select_level()
        address_id = StudentController.select_address()
        mobile = input('enter student mobile number : ')
        email = input('enter student email : ')
        fields = f""" ( mobile_number ,email )  """
        table_name = f""" contact """
        query = f""" insert  into {table_name} {fields} VALUES ({mobile} , ('{email}') )"""
        cur.execute(query)
        contact_id = cur.lastrowid
        fields = f""" ( student_name ,contact_id,address_id,level_id,BOD )  """
        table_name = f""" student """
        query = f""" insert  into {table_name} {fields} VALUES ('{name}', {contact_id} , {address_id},{level} , ('{birth_date}'))"""
        cur.execute(query)
        DbController.conn.commit()
