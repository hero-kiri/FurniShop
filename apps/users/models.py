from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# User.objects.create_user('user@example.com', 'password123')

class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        '''
        Создает и возвращает экземпляр класса User
        '''
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email) 
        user = self.model(email=email, **extra_fields) # Создает экземпляр класса
        user.set_password(password)  # Хэширует пароль
        user.save(using=self._db)  # Сохраняет в БД
        return user # Возвращает экземпляр
    
    def create_superuser(self,email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)
    
    def create(self, **kwargs):
        return super().create(**kwargs)


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    auth_code = models.CharField(max_length=4, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

