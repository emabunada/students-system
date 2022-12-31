import json

from flask import Flask, render_template, request

from controller.course_controller import CourseController
from controller.course_schedule_controller import CourseScheduleController
from controller.student_controller import StudentController

app = Flask(__name__)


@app.route("/")
def home():
    context = {'title': 'student system'}
    return render_template('index.html', **context)


@app.route("/students")
def students_table():
    students = StudentController.get_all_students()
    context = {'students': students}
    return render_template('students.html', **context)


@app.route("/courses")
def courses_table():
    courses = CourseController.get_courses()
    context = {'courses': courses}
    return render_template('courses.html', **context)


@app.route("/schedules")
def schedules_table():
    schedules = CourseScheduleController.get_all_course_schedules()

    context = {'schedules': schedules}
    return render_template('course_schedules.html', **context)


@app.route('/student_details/<int:student_id>', methods=['GET'])
def student_details(student_id):
    incomes = request.get_json()
    if incomes["API_KEY"] == '4fa86438-3478-4889-81d1-d02f24f6de25':
        student = StudentController.get_student_by_id(int(student_id))
        return {"data": student.to_json()}, 200
    else:
        return {"message": "you not authorized to use this api "}, 401


if __name__ == "__main__":
    app.run(debug=True)
