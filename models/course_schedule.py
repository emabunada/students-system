class CourseSchedule:
    def __init__(self, course_schedule_id, course_id, day, duration, start_time, level_id, course_name=''):
        self.course_schedule_id = course_schedule_id
        self.course_id = course_id
        self.level_id = level_id
        self.day = day
        self.duration = duration
        self.start_time = start_time
        self.course_name = course_name
