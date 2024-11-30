
from django.urls import path
from graphene_django.views import GraphQLView 

urlpatterns = [
    path('events/', GraphQLView.as_view(graphiql=True)),
]
