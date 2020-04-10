"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from uploadImage.views import Index, Upload, View
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', Index.as_view(), name="index"),
    path('upload/', Upload.as_view(), name="upload"),
    re_path('view/(?P<pk>\w+)/$', View.as_view(), name="view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()



"""from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from UploadImage.views import MainPage, UploadPage, ShowImage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    path('', MainPage.as_view(), name="main"),
    path('upload/', UploadPage.as_view(), name="upload"),
    re_path(r'^image/(?P<pk>\w+)/$', ShowImage.as_view(), name="image_page"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()"""