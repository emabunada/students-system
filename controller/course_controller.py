from datetime import datetime

from controller.db_controller import DbController
from controller.level_controller import LevelController
from controller.student_controller import StudentController
from models.course import Course


class CourseController(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    @staticmethod
    def course_from_tuple(x: tuple):
        course_id = int(x[0])
        level_id = int(x[1])
        course_name = x[2]
        max_capacity = int(x[3])
        rate_per_hour = float(x[4])
        return Course(course_id, course_name, level_id, max_capacity, rate_per_hour)

    @staticmethod
    def get_courses():
        query = f""" select * from course """
        DbController.cur.execute(query)
        data = list(DbController.cur)
        courses = list(map(CourseController.course_from_tuple, data))
        return courses

    @staticmethod
    def get_course_by_id(c_id):
        query = f""" select * from course where course_id = {c_id} """
        DbController.cur.execute(query)
        data = list(DbController.cur)
        if len(data) > 0:
            course = CourseController.course_from_tuple(data[0])
            return course
        else:
            print("course not found")

    @staticmethod
    def create_new_course():
        print('--------------------------------------------------------------------------------')
        c_id = input('enter course ID number:  ')
        name = input('enter course name:  ')
        level = LevelController.select_level()
        capacity = input('enter course max capacity:  ')
        rate = input('enter course hour price:  ')
        fields = f""" course_id,course_name, level_id , max_capacity ,rate_per_hour  """
        table_name = f""" course """
        query = f""" insert  into {table_name} ({fields}) VALUES ({c_id}, '{name}'  , {level},{capacity} , {rate} )"""
        DbController.cur.execute(query)
        DbController.conn.commit()

    @staticmethod
    def check_student_and_course_in_the_same_level(student, course):
        if student.level_id == course.level_id:
            return True
        else:
            print("student and course must be in the same level")
            return False

    @staticmethod
    def check_course_capacity_not_full(course):
        query = f""" select count(course_id) from enrollment_history where course_id = {course.course_id}"""
        DbController.cur.execute(query)
        data = list(DbController.cur)
        capacity = int(data[0][0])
        if capacity < int(course.max_capacity):
            return True
        else:
            print("the course reach to max capacity")
            return False

    @staticmethod
    def check_student_enroll_course_before(student, course):
        query = f""" select * from enrollment_history where student_id = {student.student_id}
         and course_id = {course.course_id}"""
        DbController.cur.execute(query)
        data = list(DbController.cur)
        if len(data) == 0:
            return True
        else:
            print("the student is already enrolled to this course")
            return False

    @staticmethod
    def perform_enroll_student_to_course(student, course, total_hour):
        print(datetime.now())
        fields = f"""(student_id,course_id,enroll_date,total_hours,total )"""
        query = f""" insert  into enrollment_history {fields} VALUES 
        ({student.student_id} , {course.course_id},('{datetime.strftime(datetime.today(), '%Y/%m/%d')}')
        ,{total_hour},{course.rate_per_hour * total_hour} ) """
        DbController.cur.execute(query)
        DbController.conn.commit()

    @staticmethod
    def enroll_course():
        print('--------------------------------------------------------------------------------')
        s_id = int(input("enter student id : "))
        student = StudentController.get_student_by_id(s_id)
        c_id = int(input("enter course id : "))
        course = CourseController.get_course_by_id(c_id)
        if student is not None and course is not None:
            if CourseController.check_student_and_course_in_the_same_level(student, course):
                if CourseController.check_student_enroll_course_before(student, course):
                    if CourseController.check_course_capacity_not_full(course):
                        total_hour = int(input("enter course total hours : "))
                        CourseController.perform_enroll_student_to_course(student, course, total_hour)
