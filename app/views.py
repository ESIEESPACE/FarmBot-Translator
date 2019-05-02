import json

import django
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

import app
from app import models
from app.forms import UploadLanguageFileForm
from app.models import Translation, Language


def index(request):
    short = request.GET.get("language", "")

    try:
        language = Language.objects.get(short=short)
        translations = Translation.objects.filter(language=language)
    except app.models.Language.DoesNotExist:
        translations = None

    languages = Language.objects.all()

    return render(request, 'table.html', context={"translations": translations, "languages": languages})

@csrf_exempt
def update_translation(request):
    short = request.POST.get("language", "")
    id = request.POST.get("id", "")
    translation = request.POST.get("translation", "")

    try:
        language = Language.objects.get(short=short)
        tr = Translation.objects.get(language=language, id=id)
        tr.translation = translation
        tr.save()
    except Exception:
        return django.http.HttpResponseBadRequest()

    return django.http.HttpResponse(status=200)


def download(request):
    short = request.GET.get("language", "fr")
    try:
        response = HttpResponse(json.dumps(bdd_to_json(short), ensure_ascii=False), content_type="application/json")
        response['Content-Disposition'] = 'attachment; filename=' + short + '.json'
        return response
    except app.models.Language.DoesNotExist:
        return django.http.HttpResponseNotFound()


def import_file(request):
    if request.method == 'POST':
        form = UploadLanguageFileForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            short = str(form.cleaned_data.get("file"))[:str(form.cleaned_data.get("file")).find(".json")]
            json_to_bdd(request.FILES['file'], name=name, short=short)
            return HttpResponseRedirect('/?language=' + short)
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


def bdd_to_json(short):
    language = Language.objects.get(short=short)
    translated = {}
    for e in Translation.objects.filter(language=language, translated=True):
        translated[e.original] = e.translation

    untranslated = {}
    for e in Translation.objects.filter(language=language, translated=False):
        untranslated[e.original] = e.translation

    other_translations = {}
    for e in Translation.objects.filter(language=language, other=True):
        other_translations[e.original] = e.translation

    result = {
        "translated": translated,
        "untranslated": untranslated,
        "other_translations": other_translations
    }

    return result
