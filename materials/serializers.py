from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import ValidatorYoutubeLink


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            ValidatorYoutubeLink(field='link')
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            ValidatorYoutubeLink(field='link')
        ]

    def get_count_lessons(self, instance):
        return Lesson.objects.filter(course=instance.id).count()

    def get_is_subscribe(self, instance):
        user = self.context['request'].user
        is_subscribed = Subscription.objects.filter(user=user, course=instance).exists()
        return is_subscribed

    def create(self, validated_data):
        new_course = Course.objects.create(**validated_data)
        new_course.owner = self.context['request'].user
        new_course.save()
        return new_course

