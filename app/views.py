from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from app.forms import UploadLanguageFileForm
from app.models import Translation, Language


def index(request):
    return render(request, 'table.html')


def import_file(request):
    if request.method == 'POST':
        form = UploadLanguageFileForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST.get("name")
            short = request.POST.get("short")

            json_to_bdd(request.FILES['file'], name=name, short=short)
            return HttpResponseRedirect('/')
    else:
        form = UploadLanguageFileForm()

    return render(request, 'upload.html', {'form': form})

def json_to_bdd(json_file, name, short):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    language = Language.objects.get(name=name, short=short)

    pass


def bdd_to_json(language):
    pass
