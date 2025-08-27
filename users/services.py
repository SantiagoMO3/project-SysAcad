"""
Servicio para la creación de usuarios y perfiles en el sistema.
Aplica SRP y OCP extrayendo la lógica de negocio de las vistas.
"""
from django.db import transaction
from users.models import CustomUser, Student, Professor, Administrator

class UserProfileService:
    @staticmethod
    @transaction.atomic
    def create_user_with_profile(user_form, profile_form, role):
        """
        Crea un usuario y su perfil asociado según el rol.
        """
        user = user_form.save()
        profile = None
        if profile_form is not None:
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
        return user, profile
