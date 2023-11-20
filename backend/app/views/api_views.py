from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from ..models import Level, Question, VocabLevel
from ..serializers import LevelSerializer, QuestionSerializer, VocabLevelSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import filters
from rest_framework.decorators import api_view
import json
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import timezone

class LevelSearch(ListAPIView):

    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name',]

class StandardResultsSetPagination(PageNumberPagination):

    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

class LevelsAll(ListAPIView):
    queryset = Level.objects.all().only('name', 'approved')
    serializer_class = LevelSerializer

class VocabularyLevelDetail(APIView):
    def get(self, reques, id=None):
        queryset = VocabLevel.objects.filter(level_id=id).all().only('level', 'name', 'description', 'example')
        vocabulary = get_list_or_404(queryset)
        serializer = VocabLevelSerializer(vocabulary, many=True)
        return Response(serializer.data)

class LevelsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    pagination_class = StandardResultsSetPagination

    lookup_field = 'slug'

    def list(self, request) -> object:
        queryset = Level.objects.filter(created__lte=timezone.now()).order_by('created')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LevelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response('')

    def retrieve(self, request, slug=None):
        queryset = Question.objects.filter(level__slug=slug)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def favorite(request):
    favorites_slugs = json.loads(request.data.get('fav'))
    queryset = Level.objects.filter(slug__in=favorites_slugs)
    serializer = LevelSerializer(queryset, many=True)
    return Response(serializer.data)
