import math
from datetime import datetime, time
from math import floor

from controller.db_controller import DbController
from models.course_schedule import CourseSchedule


class CourseScheduleController(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    @staticmethod
    def course_schedule_from_tuple(x: tuple):
        course_schedule_id = int(x[0])
        course_id = int(x[1])
        day = x[2]
        duration = int(x[3])
        start_time = (datetime.strptime(str(x[4]), '%H:%M:%S')).time()
        print(start_time)
        level_id = int(x[5])
        course_name = x[6]
        return CourseSchedule(course_schedule_id, course_id, day, duration, start_time, level_id, course_name)

    @staticmethod
    def get_course_time(message: str):
        while True:
            try:
                a = input(f'specify {message} in HH-MM format: ')
                course_time = (datetime.strptime(f'{a}-00', '%H-%M-%S')).time()
                return course_time
            except IndexError as e:
                print("Please enter correct time in HHMM format")

    @staticmethod
    def get_week_day():
        days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        while True:
            print("1: Saturday \n2: Sunday\n3: Monday\n4: Tuesday\n5: Wednesday\n6: Thursday\n7: Friday")
            day = int(input("select course day: "))
            if day in range(1, 8):
                return days[day]
            else:
                print("wrong input try again :")

    @staticmethod
    def get_integer_value_from_user(message):
        while True:
            a = input(message)
            if a.isdigit():
                return int(a)
            else:
                print("input integer numeric value")

    @staticmethod
    def add_duration_to_time(d_time: datetime.time, duration):
        hours = floor(duration / 60)
        minutes = math.ceil((duration / 60 - hours) * 60)
        if d_time.minute + minutes >= 60:
            hours += 1
            minutes = minutes + d_time.minute - 60
        end = time(hour=int(d_time.hour + hours), minute=int(minutes))
        return end

    @staticmethod
    def get_all_course_schedules():
        schedules = []
        query = f""" select cs.course_schedule_id, cs.course_id,cs.day,cs.duration,cs.start_time,c.level_id
         ,c.course_name from course_schedule as cs join course as c on cs.course_id = c.course_id """
        DbController.cur.execute(query)
        data = list(DbController.cur)
        course_schedules = list(map(CourseScheduleController.course_schedule_from_tuple, data))
        return course_schedules

    @staticmethod
    def check_intervals_interfere(first_start, first_end, second_start, second_end):
        is_interfere = False
        if first_start <= second_start <= first_end:
            is_interfere = True
        elif second_start <= first_start <= second_end:
            is_interfere = True
        elif second_start >= first_start and second_end <= first_end:
            is_interfere = True
        elif second_start <= first_start and second_end >= first_end:
            is_interfere = True

        return is_interfere

    @staticmethod
    def check_course_schedule_if_already_exists(new_start_time: datetime.time, new_course_id: int,
                                                day: str,
                                                duration: float):
        found = False
        new_end_time = CourseScheduleController.add_duration_to_time(new_start_time, duration)
        all_schedules = CourseScheduleController.get_all_course_schedules()
        for schedule in all_schedules:
            end_time = CourseScheduleController.add_duration_to_time(
                schedule.start_time,
                int(schedule.duration))
            if new_course_id == schedule.course_id:

                if schedule.day == day:

                    if CourseScheduleController.check_intervals_interfere(schedule.start_time, end_time,
                                                                          new_start_time, new_end_time):
                        print("there is interfering in the new schedule with other schedules ")
                        found = True

        return found

    @staticmethod
    def create_course_schedule():
        print('--------------------------------------------------------------------------------')
        day = CourseScheduleController.get_week_day()
        c_id = int(input("enter course id : "))
        start_time = CourseScheduleController.get_course_time("course start time")
        duration = CourseScheduleController.get_integer_value_from_user("enter course lecture duration in minutes : ")
        fields = f""" course_id,day, duration , start_time   """
        table_name = f""" course_schedule """
        query = f""" insert  into {table_name} ({fields}) VALUES ({c_id}, '{day}' , {duration},
            time('{str(start_time)}')) """
        if not CourseScheduleController.check_course_schedule_if_already_exists(start_time, c_id, day, duration):
            DbController.cur.execute(query)
            DbController.conn.commit()

    @staticmethod
    def view_student_course_schedule():
        week_schedule = {'Saturday': [], 'Sunday': [], 'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [],
                         'Friday': []}
        student_id = int(input("enter student id : "))
        query = f"""select s.student_name ,eh.student_id , c.course_name,cs.day 
        , cs.start_time , cs.duration from course_schedule as cs 
        join enrollment_history as eh join course as c
         join student as s on c.course_id = cs.course_id and cs.course_id = eh.course_id 
        and eh.student_id = s.student_id  where eh.student_id = {student_id}"""
        DbController.cur.execute(query)
        data = list(DbController.cur)
        # student_schedule = map(CourseScheduleController.course_schedule_from_tuple, data)
        print('********************************************************************************************')
        print(f"student name : {data[0][0]}")
        for row in data:
            week_schedule[str(row[3])].append(
                {'course': row[2], 'start_time': str(datetime.strptime(str(row[4]), '%H:%M:%S').time()),
                 'duration': row[5]})
        print(f"""\t\t\t\t\tCourse name\t\t\t\t\t\t\t\t\t\tStart Time\t\t\tDuration""")
        for key in week_schedule.keys():
            print(key)
            for i in range(0, len(week_schedule.get(key))):
                print(
                    f"""\t\t\t\t\t{week_schedule.get(key)[i]['course']}\t\t\t\t\t\t{week_schedule.get(key)[i]['start_time']}\t\t\t{week_schedule.get(key)[i]['duration']}""")

        print('********************************************************************************************')
