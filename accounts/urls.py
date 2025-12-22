from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 

urlpatterns = [ 
    path('',views.empty,name='home'),
    path('home/',views.home,name='home'),
    path('connect/',views.connect,name='connect'),
    path('import-wallet/', views.import_wallet_view, name='import_wallet'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
