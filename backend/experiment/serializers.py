from rest_framework import serializers
from .models import Treatment, ClassificationResult
from django.contrib.auth.models import User
from issues.serializers import UserSerializer

class TreatmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Treatment
        fields = ('name', 'label',)

class ClassificationResultSerializer(serializers.ModelSerializer):
    user = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = ClassificationResult
        fields = ('user',
            'score_autonomy', 'score_impersonal', 'score_control', 'score_amotivation',
            'age',
            'sex',
            'occupation'
        )

