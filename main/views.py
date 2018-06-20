import logging

from celery.result import AsyncResult
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from main.filters import TranslationFilter
from main.forms import TranslationForm
from main.tables import TranslationTable
from .models import Translation
import json
from main.tasks import upload_en_data_to_database, upload_es_data_to_database


def upload_json_en(request):
    try:
        json_file = request.FILES["json_file_en"]
        if not json_file.name.lower().endswith('.json'):
            messages.error(request, 'File is not JSON type')
            return HttpResponseRedirect(reverse("main:upload_json_en"))
        json_data = json.load(json_file)
        task = upload_en_data_to_database.delay(json_data)
        return render(request, 'main/upload_files.html', {'task_id': task.id})

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))
        error = "Unable to upload file. " + repr(e)
        return render(request, "main/upload_files.html", {'error': error})



def upload_json_es(request):
    try:
        json_file = request.FILES["json_file_es"]
        if not json_file.name.lower().endswith('.json'):
            messages.error(request, 'File is not JSON type')
            return HttpResponseRedirect(reverse("main:upload_json_es"))
        json_data = json.load(json_file)
        task = upload_es_data_to_database.delay(json_data)
        return render(request, 'main/upload_files.html', {'task_id': task.id})

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))
        error = "Unable to upload file. " + repr(e)
        return render(request, "main/upload_files.html", {'error': error})


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

def get_progress(request):
    if 'task_id' in request.GET:
        task_id = request.GET['task_id']
    else:
        return HttpResponse('No job id given.')
    result = AsyncResult(task_id)
    response_data = {
        'state': result.state,
        'details': result.info,
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')