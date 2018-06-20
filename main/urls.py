from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.FilteredTranslationListView.as_view(), name='translation_list'),
    url(r'^upload_files/$', views.upload_files, name='upload_files'),
    url(r'^upload/json_en/$', views.upload_json_en, name='upload_json_en'),
    url(r'^upload/json_es/$', views.upload_json_es, name='upload_json_es'),
    url(r'^translation/(?P<pk>\d+)/edit/$', views.translation_edit, name='translation_edit'),
    url(r'^download_files/$', views.download_files, name='download_files'),
    url(r'^download/json_es/$', views.download_json, name='download_json'),
]