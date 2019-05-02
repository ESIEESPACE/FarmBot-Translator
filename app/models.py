from django.db import models


# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=50)
    short = models.CharField(max_length=5)

    def __str__(self):
        return self.name+" ("+self.short+")"


class Translation(models.Model):
    position = models.IntegerField()
    original = models.TextField()
    translation = models.TextField()
    translated = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.SET(None))

    def __str__(self):
        return self.position+ " : "+self.language