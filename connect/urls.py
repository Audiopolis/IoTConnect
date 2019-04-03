from django.urls import path

from connect.views import ConnectView, DataportenRedirectView

urlpatterns = [
    path('', ConnectView.as_view(), name='connect'),
    path('complete/dataporten/', DataportenRedirectView.as_view(), name='dataporten-redirect'),
]
