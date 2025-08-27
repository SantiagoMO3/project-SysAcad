"""Core user and profile models.

Defines:
- CustomUser: extends Django's AbstractUser with role and identity fields.
- Student: one-to-one profile linked to a Career.
- Professor: one-to-one profile with teaching assignments and category.
- Administrator: one-to-one profile for administrative staff.

Notes:
    - db_table is set for each model to keep stable table names.
    - One-to-one relations ensure a single profile per CustomUser.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user extending AbstractUser with roles and identity fields.

    Attributes:
        role (str): One of Role choices: {'administrator', 'professor', 'student'}.
        dni (str): National ID; unique.
        phone (str | None): Optional phone number.
        birth_date (date | None): Optional birth date.
        address (str | None): Optional address.
    """

    class Role(models.TextChoices):
        """User roles in the system."""
        ADMIN = 'administrator', 'Administrator'
        PROFESSOR = 'professor', 'Professor'
        STUDENT = 'student', 'Student'

    role = models.CharField(max_length=20, choices=Role.choices, blank=False, null=False)
    dni = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        """Meta options for CustomUser."""
        db_table = 'users'

    def __str__(self):
        """Return full name for admin readability."""
        return f"{self.get_full_name()}"



# Clase base abstracta para perfiles de usuario
class UserProfile(models.Model):
    """
    Clase base abstracta para perfiles de usuario.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hire_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


# Perfil de estudiante
class Student(UserProfile):
    """
    Student profile linked one-to-one with a CustomUser.
    """
    student_id = models.CharField(max_length=20, unique=True, primary_key=True)
    career = models.ForeignKey('academics.Career', on_delete=models.SET_NULL, null=True, related_name='students')
    enrollment_date = models.DateField()

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"Student ID {self.student_id} - {self.user.get_full_name()}"



# Perfil de profesor
class Professor(UserProfile):
    """
    Professor profile with subjects/final exams assignments.
    """
    class Category(models.TextChoices):
        TITULAR = 'titular', 'Titular'
        ADJUNCT = 'adjunct', 'Adjunct'
        AUXILIAR = 'auxiliar', 'Auxiliar'

    professor_id = models.CharField(max_length=20, unique=True, primary_key=True)
    subjects = models.ManyToManyField('academics.Subject', related_name='professors', blank=True)
    final_exams = models.ManyToManyField('academics.FinalExam', related_name='professors', blank=True)
    degree = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices)

    class Meta:
        db_table = 'professors'

    def __str__(self):
        return f"{self.user.get_full_name()}"



# Perfil de administrador
class Administrator(UserProfile):
    """
    Administrator profile for non-teaching staff.
    """
    administrator_id = models.CharField(max_length=20, unique=True, primary_key=True)
    position = models.CharField(max_length=100)

    class Meta:
        db_table = 'administrators'

    def __str__(self):
        return f"{self.user.get_full_name()}"
