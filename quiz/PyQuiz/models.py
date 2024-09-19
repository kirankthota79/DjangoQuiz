from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # User
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

# Create your models here.

class Address(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60, default="")
    state = models.CharField(max_length=30, default="")
    postcode = models.CharField(max_length=6, default="")
    country = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = " Address"
        # app_label = "PyQuiz"
        
    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            is_staff = is_staff,
            is_active = True,
            is_superuser = is_superuser,
            last_login = now, 
            date_joined= now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using= self._db)
        return user
    
    # class Meta:
    #     app_label = "PyQuiz"
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null= True, blank= True)
    username = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    
class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, default=None)
    address = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    
    def __str__(self):
        return f"{self.user.name} Profile"
    
    def save(self,*args, **kwargs):      # (self, *args, **kwargs
        super().save(*args, **kwargs)
        
@receiver(post_save, sender= User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwards):
    instance.profile.save()
    
 
    
"""
class Quiz(models.Model):
    
    Type =( 
           (1, "radio"),
           (2, "Multiple answer")
           )
    Question = models.CharField(max_length=255)
    Answer = models.CharField(max_length=20, choices=Type, default="radio")
    author = models.ForeignKey(User, on_delete= models.CASCADE)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        
    def __str__(self):
        return self.Question

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})
# )
"""