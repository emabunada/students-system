from flask import Flask, render_template, request

from controller.course_controller import CourseController
from controller.course_schedule_controller import CourseScheduleController
from controller.student_controller import StudentController

# http://staging.bldt.ca/api/method/build_it.user_api.home.get_home


app = Flask(__name__)
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True


@app.route("/")
def home():
    context = {'title': 'student system'}
    return render_template('index.html', **context)


@app.route("/students")
def students_table():
    students = StudentController.get_all_students()
    for s in students:
        print(s.BOD)
    context = {'students': students}
    return render_template('students.html', **context)


@app.route("/courses")
def courses_table():
    courses = CourseController.get_courses()
    for c in courses:
        print(c.course_name)
    context = {'courses': courses}
    return render_template('courses.html', **context)


@app.route("/schedules")
def schedules_table():
    schedules = CourseScheduleController.get_all_course_schedules()
    for s in schedules:
        print(s.course_name)
    context = {'schedules': schedules}
    return render_template('course_schedules.html', **context)


@app.route('/student_details', methods=['GET'])
def student_details():
    incomes = [request.get_json()]
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)
