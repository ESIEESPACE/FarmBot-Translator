import json

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from app import models
from app.forms import UploadLanguageFileForm
from app.models import Translation, Language


def index(request):

    short = request.GET.get("language", "fr")

    language = Language.objects.get(short=short)
    translations = Translation.objects.filter(language=language)

    languages = Language.objects.all()

    return render(request, 'table.html', context={"translations": translations, "languages": languages})


def import_file(request):
    if request.method == 'POST':
        form = UploadLanguageFileForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            short = str(form.cleaned_data.get("file"))[:str(form.cleaned_data.get("file")).find(".json")]
            json_to_bdd(request.FILES['file'], name=name, short=short)
            #return HttpResponseRedirect('/')
    else:
        form = UploadLanguageFileForm()

    return render(request, 'upload.html', {'form': form})


def json_to_bdd(json_file, name, short):
    """with open('some/file/name.txt', 'wb+') as destination:
        for chunk in json_file.chunks():
            destination.write(chunk)"""

    decoded_json = json.loads(json_file.read())

    try:
        language = Language.objects.get(short=short)
    except models.Language.DoesNotExist:
        language = Language.objects.create(name=name, short=short)

    translated = [{'original': k, 'translation': v} for k, v in decoded_json.get("translated").items()]
    untranslated = [{'original': k, 'translation': ''} for k, v in decoded_json.get("untranslated").items()]
    other_translations = [{'original': k, 'translation': ''} for k, v in decoded_json.get("other_translations").items()]

    i = 0
    for e in translated:
        k = e.get('original')
        v = e.get('translation')
        Translation.objects.create(position=i, original=k, translation=v, translated=True, language=language)
        i += 1

    i = 0
    for e in untranslated:
        k = e.get('original')
        v = e.get('translation')
        Translation.objects.create(position=i, original=k, translation=v, language=language)
        i += 1

    i = 0
    for e in other_translations:
        k = e.get('original')
        v = e.get('translation')
        Translation.objects.create(position=i, original=k, translation=v, other=False, language=language)
        i += 1


def bdd_to_json(language):
    pass
