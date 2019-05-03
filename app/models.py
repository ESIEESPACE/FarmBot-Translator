from django.db import models


# Create your models here.
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
