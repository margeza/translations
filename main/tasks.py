from difflib import SequenceMatcher

from celery import current_task

from main.models import Translation
from translations.celery import app

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def get_translation_status(key, english_translation, spanish_translation):
    if english_translation == spanish_translation:
        return Translation.TODO
    elif similar(english_translation, spanish_translation) > 0.7:
        return Translation.SIMILAR
    elif (spanish_translation != english_translation and spanish_translation != ""):
        return Translation.DONE
    else:
        return Translation.TODO

def add_en_line_to_database(key, value):
    Translation.objects.create(key=key,
                               english_translation=value,
                               spanish_translation="",
                               status=Translation.TODO)

@app.task
def upload_en_data_to_database(en_json):
    total_work_to_do = len(en_json)
    Translation.objects.all().delete()
    for i, (key, value) in enumerate(en_json.items()):
        add_en_line_to_database(key, value)
        current_task.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': total_work_to_do})

def add_es_line_to_database(key, value):
    english_translation = Translation.objects.get(key=key).english_translation
    status = get_translation_status(key, english_translation, value)
    Translation.objects.filter(key=key).update(spanish_translation=value, status=status)

@app.task
def upload_es_data_to_database(es_json):
    total_work_to_do = len(es_json)
    for i, (key, value) in enumerate(es_json.items()):
        add_es_line_to_database(key, value)
        current_task.update_state(state='PROGRESS',
            meta={'current': i, 'total': total_work_to_do})


