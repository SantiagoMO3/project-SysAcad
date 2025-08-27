"""
Servicio para obtener los datos de la ficha del alumno.
Aplica SRP y OCP.
"""
from users.models import Student

class StudentRecordService:
    @staticmethod
    def get_student_record(user):
        student = Student.objects.select_related('career__faculty', 'user').filter(user=user).first()
        if not student:
            return None
        return {
            'student_id': student.student_id,
            'last_name': student.user.last_name,
            'first_name': student.user.first_name,
            'dni': student.user.dni,
            'career': student.career.name if student.career else '',
            'faculty': student.career.faculty.name if student.career and student.career.faculty else ''
        }
