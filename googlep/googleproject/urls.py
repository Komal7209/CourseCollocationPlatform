from django.conf.urls import url
from googleproject import views

#for images and static files
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns=[
    url(r'^$',views.index,name='index'),
]

#fxn to add path of static files
urlpatterns+=staticfiles_urlpatterns()