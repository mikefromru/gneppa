from rest_framework import serializers
from . models import Level, Question, VocabLevel

class LevelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Level
        fields = '__all__'

        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

class VocabLevelSerializer(serializers.ModelSerializer):

    class Meta:

        model = VocabLevel
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Question
        fields = '__all__'
