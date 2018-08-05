# -*- coding: utf-8 -*-
from .views import PrivateGraphQLView, downloadExcel
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token


urlpatterns = [
    url(r'^graphql', csrf_exempt(PrivateGraphQLView.as_view(graphiql=True))),
    url(r'^refresh-token', refresh_jwt_token),
    url(r'^login', obtain_jwt_token),
    url(r'^download', csrf_exempt(downloadExcel)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
