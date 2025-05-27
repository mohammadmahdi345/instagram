from django.core import validators
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save

class CreatedTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    """منیجر یوزر سفارشی که در اون به غیر از یوزرنیم و پسورد به ایمیل یا شماره تلفن کاربر هم نیاز داریم"""

    def create_user(self,username=None, phone_number=None, password=None,email=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError('وارد کردن شماره تلفن یا ایمیل الزامی است.')
        user = self.model(username=username,phone_number=phone_number,email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, phone_number, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, phone_number, password, email, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """ یوزر سفارشی که دارای ویلیدتور های خاصی برای فیلدهاس """
    username = models.CharField('username', max_length=32, unique=True,
                                help_text=
                                    'Required. 30 characters or fewer starting with a letter. Letters, digits and underscore only.',
                                validators=[
                                    validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                                              'Enter a valid username starting with a-z. '
                                                                'This value may contain only letters, numbers '
                                                                'and underscore characters.', 'invalid'),
                                ],
                                error_messages={
                                    'unique': "A user with that username already exists.",
                                }
                                )
    phone_number = models.CharField('mobile number',max_length=13,null=True, blank=True,
                                          validators=[
                                              validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                        ('Enter a valid mobile number.'), 'invalid'),
                                          ],                                          error_messages={
                                              'unique': "A user with this mobile number already exists.",
                                          }
                                          )
    email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=30, blank=True)
    is_banned = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    receive_post_notifications = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number','password','email']

    def __str__(self):
        return str(self.username)

class Profile(models.Model):
    """پروفایل کاربر که شامل فیلد های زیره"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/profile/', blank=True,null=True)
    post = models.ManyToManyField('post.Post',blank=True,related_name='posts', null=True)
    bio = models.CharField(max_length=560, blank=True, null=True)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    """بعد ثبت نام کاربر براش پروفایل میسازیم"""
    if created:
        profile = Profile(user=instance.user)
        profile.save()

post_save.connect(create_profile, sender=User)


class Bookmark(CreatedTime):
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='bookmark')
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='bookmark_post')
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') # برای اینکه یک کاربر یک پست یکسان رو ذخیره نکنه
        ordering = ['-created_at']


