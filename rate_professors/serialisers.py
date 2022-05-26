from django.contrib.auth import get_user_model
from django.contrib.auth.backends import UserModel
from rest_framework import serializers

from .models import Professor, Module, Rating


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ('code',
                  'name',
                  )


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    professor = ProfessorSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Module
        fields = ('code',
                  'name',
                  'year',
                  'semester',
                  'professor',
                  )


class PostRatingSerializer(serializers.ModelSerializer):
    # professor = ProfessorSerializer()
    #
    # module = ModuleSerializer()

    class Meta:
        model = Rating
        fields = ('professor',
                  'module',
                  'rating',
                  )


class GetRatingSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer()

    module = ModuleSerializer()

    class Meta:
        model = Rating
        fields = ('professor',
                  'module',
                  'rating',
                  )