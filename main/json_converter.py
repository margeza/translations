import json
from difflib import SequenceMatcher

from main.models import Translation


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


def load_en_json(en_json):
    Translation.objects.all().delete()

    english_version = json.load(en_json)

    for key, value in english_version.items():
        Translation.objects.create(key=key,
                                   english_translation=value,
                                   spanish_translation="",
                                   status=Translation.TODO)


def load_es_json(es_json):
    spanish_version = json.load(es_json)

    for key, value in spanish_version.items():
        english_translation = Translation.objects.get(key=key).english_translation
        status = get_translation_status(key, english_translation, value)
        Translation.objects.filter(key=key).update(spanish_translation=value, status=status)