import shortuuid
from shortuuid.django_fields    import ShortUUIDField
from django.contrib.auth.models import AbstractUser
from django.utils               import timezone
from django.db                  import models


def user_profule_picture(instance,filename):
  return f'users/user_{instance.code}/{shortuuid.uuid()}.{str(filename).split('.')[1]}'


class User(AbstractUser):
  code             = ShortUUIDField(unique=True,length=4,max_length=10,prefix='us',alphabet='1234567890')
  image            = models.ImageField(upload_to=user_profule_picture,blank=True,null=True)
  data_cricao      = models.DateTimeField(default=timezone.now)
  data_atulizacao  = models.DateTimeField(auto_now=True)

  REQUIRED_FIELDS = []

  def __str__(self):
    return self.username