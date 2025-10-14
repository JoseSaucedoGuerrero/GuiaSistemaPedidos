from django.contrib.auth.models import BaseUserManager
from . import constants as user_constants

class UserManager(BaseUserManager): 
    def create_user(self, username, email, full_name, perfil_id, mobile='', password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        
        if not perfil_id:
            raise ValueError('Se requiere el perfil del usuario')
        
        user = self.model(
            username=username,
            full_name=full_name,
            email=self.normalize_email(email),
            perfil_id=perfil_id,
            mobile=mobile
        )
        
        if not password:
            from django.contrib.auth.models import User
            password = User.objects.make_random_password(length=8, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")
        
        user.set_password(password)
        user.is_superuser = extra_fields.get('is_superuser', False)
        user.is_staff = extra_fields.get('is_staff', True)
        user.is_active = extra_fields.get('is_active', True)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        
        # Obtener perfil_id, full_name y mobile de extra_fields
        perfil_id = extra_fields.pop('perfil_id', user_constants.ADMINISTRADOR)
        full_name = extra_fields.pop('full_name', username)
        mobile = extra_fields.pop('mobile', '')
        
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(
            username=username,
            email=email,
            full_name=full_name,
            perfil_id=perfil_id,
            mobile=mobile,
            password=password,
            **extra_fields
        )
    
    def update_user(self, data_user):
        iduser = data_user.get('username')
        usuario = self.filter(pk=iduser).update(
            full_name=data_user.get('full_name'),
            email=self.normalize_email(data_user.get('email')),
            perfil_id=data_user.get('perfil_id'),
            mobile=data_user.get('mobile')
        )
        
        return usuario