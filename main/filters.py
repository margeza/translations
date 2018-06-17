import django_filters
from main.models import Translation

class TranslationFilter(django_filters.FilterSet):
    class Meta:
        model = Translation
        fields = ['status']



