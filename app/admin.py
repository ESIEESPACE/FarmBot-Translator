from django.contrib import admin

# Register your models here.
from app.models import Language, Translation

class TranslationAdmin(admin.ModelAdmin):
    search_fields = ('original', 'translation', 'translated')
    list_display = ('original', 'translation', 'translated', 'other', 'user', 'updated_at')
    list_filter = ('user', 'translated')

admin.site.register(Language)
admin.site.register(Translation, TranslationAdmin)