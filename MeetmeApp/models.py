from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import cloudinary
from cloudinary.models import CloudinaryField
from django.conf import settings
from PIL import Image
from django.utils.translation import ugettext_lazy as _ 
from django.utils.timezone import utc
import datetime
import stripe
from tinymce.models import HTMLField

# Create your models here.
class Message(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver", null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author} Message to {self.receiver}'

    def get_absolute_url(self):
        return reverse("date-page")
    
# Create your models here.
GENDER_TYPE = (
	('M', 'Male'),
	('F', 'Female'),
    ('Other', 'Other')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=50,choices=GENDER_TYPE)
    # profile_pic = CloudinaryField('image', default="default.jpg", blank=True, null=True)
    more_about_myself = models.TextField(null=True)
    career = models.CharField(max_length=500, null=True)
    created_on = models.DateTimeField('Created on', auto_now_add=True)
	# updated_on = models.DateTimeField('Updated on', auto_now_add=True)
    likeability = models.ManyToManyField(User, related_name="likes", blank=True)
    blocked_by = models.ManyToManyField(User, related_name="blocked", blank=True)
    
class meta:
    profile_pic = CloudinaryField('image', default="default.jpg", blank=True, null=True)


    def __str__(self):
        return f"{self.full_name} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 250 or img.width > 250:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)

    @property
    def num_likes(self):
        return self.likeability.all().count()


class Dating(models.Model):
    lady_seeking  = models.ForeignKey(User, verbose_name=_("Lady seeking"), related_name="user_lady_seeking", on_delete=models.CASCADE)
    guy_seeking = models.ForeignKey(User, verbose_name=_("Guy_seeking"), related_name="user_guy_seeking", on_delete=models.CASCADE)
    
class Meta:
		verbose_name = _("Dating")
