import redis

from controller.course_controller import CourseController
from controller.course_schedule_controller import CourseScheduleController
from controller.student_controller import StudentController

run = True
redis_controller = redis.Redis()


def handle_choice(user_choice):
    if user_choice == '0':
        StudentController.get_all_students()
    elif user_choice == '1':
        StudentController.register_new_student()
    elif user_choice == '2':
        CourseController.enroll_course()
    elif user_choice == '3':
        CourseController.create_new_course()
    elif user_choice == '4':
        CourseScheduleController.create_course_schedule()
    elif user_choice == '5':
        CourseScheduleController.view_student_course_schedule()
        # register_new_student()
    # else:
    #     print('wrong choice please try again: ')


def main_menu():
    print('--------------------------------------------------------------------------------')
    print('1.  Register new student ')
    print('2.  Enroll course ')
    print('3.  Create new course ')
    print('4.  Create new schedule ')
    print('5.  Display student course schedule   ')
    print('0.  to exit')
    return input('please enter your choice:  ')


# Start execution

while run:
    choice = main_menu()
    handle_choice(choice)

# def get_integer_value_from_user(message):
#     while True:
#         a = input(message)
#         if a.isdigit():
#             return int(a)
#         else:
#             print("input integer numeric value")


# def get_course_time(message: str):
#     while True:
#         try:
#             a = input(f'specify {message} in HH-MM format: ')
#             course_time = datetime.strptime(f'{a}-00', '%H-%M-%S')
#             print(course_time.time())
#             return course_time
#         except IndexError as e:
#             print("Please enter correct time in HHMM format")


# def get_course_by_id(c_id):
#     query = f""" select * from course where course_id = {c_id} """
#     cur.execute(query)
#     data = list(cur)
#     if len(data) > 0:
#         return {'course_id': data[0][0], 'level_id': data[0][1], 'course_name': data[0][2], 'max_capacity': data[0][3],
#                 'rate_per_hour': data[0][4], }
#     else:
#         print("course not found")

#
# def get_student_by_id(s_id):
#     query = f""" select * from student where student_id = {s_id} """
#     cur.execute(query)
#     data = list(cur)
#     if len(data) > 0:
#         return {'student_id': data[0][0], 'student_name': data[0][1], 'contact_id': data[0][2],
#                 'address_id': data[0][3],
#                 'level_id': data[0][4], 'DOB': data[0][5], }
#     else:
#         print("student not found")

#
# def get_week_day():
#     days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#     while True:
#         print("1: Saturday \n2: Sunday\n3: Monday\n4: Tuesday\n5: Wednesday\n6: Thursday\n7: Friday")
#         day = int(input("select course day: "))
#         if day in range(1, 8):
#             return days[day]
#         else:
#             print("wrong input try again :")


# def add_duration_to_time(d_time: datetime.time, duration):
#     hours = floor(duration / 60)
#     minutes = math.ceil((duration / 60 - hours) * 60)
#     if d_time.minute + minutes >= 60:
#         hours += 1
#         minutes = minutes + d_time.minute - 60
#     end = time(hour=int(d_time.hour + hours), minute=int(minutes))
#     return end


# def get_all_course_schedules():
#     schedules = []
#     query = f""" select cs.course_id,cs.day,cs.duration,cs.start_time,c.level_id
#      from course_schedule as cs join course as c on cs.course_id = c.course_id """
#     cur.execute(query)
#     data = list(cur)
#     for row in data:
#         print(row)
#         schedules.append({'course_id': row[0], 'day': row[1], 'duration': row[2],
#                           'start_time': str(row[3]), 'level_id': row[4]})
#     print(schedules)
#     return schedules


# def check_intervals_interfere(first_start, first_end, second_start, second_end):
#     is_interfere = False
#     if first_start <= second_start <= first_end:
#         is_interfere = True
#     elif second_start <= first_start <= second_end:
#         is_interfere = True
#     elif second_start >= first_start and second_end <= first_end:
#         is_interfere = True
#     elif second_start <= first_start and second_end >= first_end:
#         is_interfere = True
#
#     return is_interfere


# def check_course_schedule_if_already_exists(new_start_time: datetime.time, new_level: int, new_course_id: int, day: str,
#                                             duration: float):
#     found = False
#     new_end_time = add_duration_to_time(new_start_time, duration)
#     all_schedules = get_all_course_schedules()
#     for schedule in all_schedules:
#         print(schedule["start_time"].split(',')[0])
#         end_time = add_duration_to_time(datetime.strptime(schedule["start_time"], '%H:%M:%S'),
#                                         int(schedule["duration"]))
#         if new_course_id == schedule["course_id"]:
#             if new_level == schedule["level_id"]:
#                 if schedule["day"] == day:
#                     if check_intervals_interfere(schedule["start_time"], end_time, new_start_time, new_end_time):
#                         print("there is interfering in the new schedule with other schedules ")
#                         found = True
#
#     return found


# def create_course_schedule():
#     print('--------------------------------------------------------------------------------')
#     day = get_week_day()
#     c_id = int(input("enter course id : "))
#     start_time = get_course_time("course start time")
#     print(start_time.strftime('%H-%M'))
#     duration = get_integer_value_from_user("enter course lecture duration in minutes : ")
#     level = LevelController.select_level()
#     fields = f""" course_id,day, duration , start_time   """
#     table_name = f""" course_schedule """
#     query = f""" insert  into {table_name} ({fields}) VALUES ({c_id}, '{day}' , {duration},
#     time('{str(start_time.time())}')) """
#     if not check_course_schedule_if_already_exists(start_time, level, c_id, day, duration):
#         print(query)
#         cur.execute(query)
#         conn.commit()


# def check_student_and_course_in_the_same_level(student, course):
#     if student['level_id'] == course["level_id"]:
#         return True
#     else:
#         print("student and course must be in the same level")
#         return False

#
# def check_student_enroll_course_before(student, course):
#     query = f""" select * from enrollment_history where student_id = {student['student_id']}
#      and course_id = {course['course_id']}"""
#     cur.execute(query)
#     data = list(cur)
#     if len(data) == 0:
#         return True
#     else:
#         print("the student is already enrolled to this course")
#         return False

#
# def check_course_capacity_not_full(course):
#     query = f""" select count(course_id) from enrollment_history where course_id = {course['course_id']}"""
#     cur.execute(query)
#     data = list(cur)
#     capacity = int(data[0][0])
#     if capacity < int(course['max_capacity']):
#         return True
#     else:
#         print("the course reach to max capacity")
#         return False


# def perform_enroll_student_to_course(student, course, total_hour):
#     print(datetime.now())
#     fields= f"""(student_id,course_id,enroll_date,total_hours,total )"""
#     query = f""" insert  into enrollment_history {fields} VALUES
#     ({student['student_id']} , {course['course_id']},('{datetime.strftime(datetime.today(),'%Y/%m/%d')}')
#     ,{total_hour},{course['rate_per_hour'] * total_hour} ) """
#     print(query)
#     cur.execute(query)

#
# def enroll_course():
#     print('--------------------------------------------------------------------------------')
#     s_id = int(input("enter student id : "))
#     student = get_student_by_id(s_id)
#     c_id = int(input("enter course id : "))
#     course = get_course_by_id(c_id)
#     if student is not None and course is not None:
#         if check_student_and_course_in_the_same_level(student, course):
#             if check_student_enroll_course_before(student, course):
#                 if check_course_capacity_not_full(course):
#                     total_hour = int(input("enter course total hours : "))
#                     perform_enroll_student_to_course(student, course, total_hour)
