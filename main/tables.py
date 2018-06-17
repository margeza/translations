import django_tables2 as tables
from .models import Translation

class TranslationTable(tables.Table):
    class Meta:
        model = Translation
        template_name = 'django_tables2/bootstrap.html'
        fields = ('key', 'english_translation', 'spanish_translation', 'status')

    my_column = tables.TemplateColumn(verbose_name='Edit',
                                      template_name='main/table_edit_column.html')