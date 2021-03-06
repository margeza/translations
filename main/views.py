import logging
from difflib import SequenceMatcher
from multiprocessing import Process

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableMixin

from main.filters import TranslationFilter
from main.forms import TranslationForm
from main.json_converter import load_en_json, load_es_json
from main.tables import TranslationTable
from .models import Translation
import json
#
# def translation_list(request):
#     translations = Translation.objects.filter(status=False)
#     table = TranslationTable(translations)
#     RequestConfig(request).configure(table)
#     return render(request, 'main/translation_filter.html', {'table': table})


def upload_json_en(request):
    data = {}
    if "GET" == request.method:
        return render(request, "main/translation_filter.html", data)
    # if not GET, then proceed
    try:
        json_file = request.FILES["json_file_en"]
        if not json_file.name.lower().endswith('.json'):
            messages.error(request, 'File is not JSON type')
            return HttpResponseRedirect(reverse("main:upload_json_en"))

        load_en_json(json_file)

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("main:translation_list"))

def upload_json_es(request):
    data = {}
    if "GET" == request.method:
        return render(request, "main/translation_filter.html", data)
    # if not GET, then proceed
    try:
        json_file = request.FILES["json_file_es"]
        if not json_file.name.lower().endswith('.json'):
            messages.error(request, 'File is not JSON type')
            return HttpResponseRedirect(reverse("main:upload_json_es"))

        load_es_json(json_file)
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("main:translation_list"))



def translation_edit(request, pk):
    translation = get_object_or_404(Translation, pk=pk)
    if request.method == "POST":
        form = TranslationForm(request.POST, instance=translation)
        if form.is_valid():
            translation = form.save(commit=False)
            translation.save()
            return redirect('main:translation_list')
    else:
        form = TranslationForm(instance=translation)
    return render(request, 'main/translation_edit.html', {'form': form})

def download_json(request):
    translations = Translation.objects.all()
    spanish_transl = {}
    for translation in translations:
        spanish_transl[translation.key] = translation.spanish_translation
    return HttpResponse(json.dumps(spanish_transl, ensure_ascii=False, indent=0), content_type="application/json")

def upload_files(request):
    return render(request, 'main/upload_files.html')

def download_files(request):
    return render(request, 'main/download_files.html')

class FilteredTranslationListView(SingleTableMixin, FilterView):
    table_class = TranslationTable
    model = Translation
    template_name = 'translation_filter.html'

    filterset_class = TranslationFilter