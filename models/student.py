class Student:
    def __init__(self, student_id, name, contact_id, address_id, level_id, bod, email='', phone='', city=''):
        self.student_id = student_id
        self.name = name
        self.contact_id = contact_id
        self.address_id = address_id
        self.level_id = level_id
        self.BOD = bod
        self.email = email
        self.phone = phone
        self.city = city

    def to_json(self):
        return {
            'student_id': self.student_id,
            'student_name': self.name,
            'contact_id': self.contact_id,
            'address_id': self.address_id,
            'level_id': self.level_id,
            'BOD': self.BOD,

        }
