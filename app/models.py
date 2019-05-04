from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Language(models.Model):
    name = models.CharField(max_length=50)
    short = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name+" ("+self.short+")"


class Translation(models.Model):
    position = models.IntegerField()
    original = models.TextField()
    translation = models.TextField()
    translated = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.SET(None))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.translated:
            state = "Translated"
        else:
            if self.other:
                state = "Other"
            else:
                state = "Untranslated"

        return str(self.language)+" : "+state+" : "+str(self.position)


class Profile(models.Model):
    user = models.OneToOneField(User,unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()