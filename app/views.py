import json

import django
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.formats import localize
from django.views.decorators.csrf import csrf_exempt

import app
from app import models
from app.forms import UploadLanguageFileForm, UserForm, ProfileForm
from app.mercure import Mercure
from app.models import Translation, Language

@login_required
def index(request):
    short = request.GET.get("language", "")

    try:
        language = Language.objects.get(short=short)
        translations = Translation.objects.filter(language=language).order_by('translated')

        translated = translations.filter(translated=True).count()
        total_translations = translations.count()

    except app.models.Language.DoesNotExist:
        translations = None
        translated = None
        total_translations = None

    languages = Language.objects.all()

    m = Mercure(short)
    config={"hubURL": m.hub_url, "topic": m.topic}
    return render(request, 'table.html', context={"translations": translations, "languages": languages, "translated": translated, "total_translations": total_translations, 'config': config})

@csrf_exempt
def update_translation(request):
    short = request.POST.get("language", "")
    id = request.POST.get("id", "")
    translation = request.POST.get("translation", "")
    
    if translation == "":
        return django.http.HttpResponseBadRequest()

    try:
        language = Language.objects.get(short=short)
        tr = Translation.objects.get(language=language, id=id)
        tr.translation = translation
        tr.user = request.user
        tr.translated = True
        tr.save()

        try:
            m = Mercure(short)
            m.hub_url = 'http://mercure:80/hub'
            m.send(json.dumps({'id': tr.id, 'translation': tr.translation, 'updated_at': localize(tr.updated_at)}))
        except Exception as e:
            print(e)
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

@login_required
def import_file(request):
    if request.method == 'POST':
        form = UploadLanguageFileForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            short = str(form.cleaned_data.get("file"))[:str(form.cleaned_data.get("file")).find(".json")]
            json_to_bdd(request.FILES['file'], name=name, short=short, user=request.user)
            return HttpResponseRedirect('/?language=' + short)
    else:
        form = UploadLanguageFileForm()

    return render(request, 'upload.html', {'form': form})


def json_to_bdd(json_file, name, short, user):
    decoded_json = json.loads(json_file.read())

    try:
        language = Language.objects.get(short=short)
    except models.Language.DoesNotExist:
        language = Language.objects.create(name=name, short=short, user=user)

    translated = [{'original': k, 'translation': v} for k, v in decoded_json.get("translated").items()]
    untranslated = [{'original': k, 'translation': ''} for k, v in decoded_json.get("untranslated").items()]
    other_translations = [{'original': k, 'translation': ''} for k, v in decoded_json.get("other_translations").items()]

    i = 0
    for e in translated:
        k = e.get('original')
        v = e.get('translation')
        try:            
            tr = Translation.objects.get(original=k, language=language)        
            tr.translation = v
            tr.translated = True
            tr.save()
        except app.models.Translation.DoesNotExist:        
            Translation.objects.create(position=i, original=k, translation=v, translated=True, language=language)
        i += 1

    i = 0
    for e in untranslated:
        k = e.get('original')
        v = e.get('translation')
        try:            
            Translation.objects.get(original=k, language=language)        
        except app.models.Translation.DoesNotExist:        
            Translation.objects.create(position=i, original=k, translation=v, language=language)
        i += 1

    i = 0
    for e in other_translations:
        k = e.get('original')
        v = e.get('translation')
        try:            
            Translation.objects.get(original=k, language=language)   
        except app.models.Translation.DoesNotExist:        
            Translation.objects.create(position=i, original=k, translation=v, other=True, language=language)
        i += 1


def bdd_to_json(short):
    language = Language.objects.get(short=short)
    translated = {}
    for e in Translation.objects.filter(language=language, translated=True, other=False):
        translated[e.original] = e.translation

    untranslated = {}
    for e in Translation.objects.filter(language=language, translated=False, other=False):
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


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'home/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def login(request):
    return render(request, 'login.html')

@login_required
def leaderboard(request):
    users = Translation.objects.all().filter(user_id__isnull=False).values('user__username').annotate(count=Count('user')).order_by('-count')
    return render(request, 'leaderboard.html', context={'users': users})