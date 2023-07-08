from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import api_views

router = DefaultRouter()
router.register(r'', api_views.LevelsViewSet, basename='fluent')

api_urlpatterns = [
    path('search/', api_views.LevelSearch().as_view()),
    path('favorite/', api_views.favorite),
    path('all/', api_views.LevelsAll.as_view()),
    path('vocabulary/<int:id>/', api_views.VocabularyLevelDetail.as_view()),
]
api_urlpatterns += router.urls
