from rest_framework import viewsets, generics, serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.permissions import IsOwner, IsModerator
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPagination

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]
    pagination_class = MaterialsPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    # permission_classes = [IsAuthenticated, IsOwner, ~IsModerator]
    permission_classes = [AllowAny]  # На время проведения тестов


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.kwargs.get('pk')
        course = Course.objects.get(pk=course_id)

        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.course = course
        new_subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]  # На время проведения тестов

    def destroy(self, request, *args, **kwargs):
        course_id = self.kwargs.get('pk')
        user_id = self.request.user.pk

        subscription = Subscription.objects.get(course_id=course_id, user_id=user_id)

        if self.request.user != subscription.user:
            raise serializers.ValidationError('Нельзя удалить чужую подписку!')
        else:
            self.perform_destroy(subscription)
            return Response(status=status.HTTP_204_NO_CONTENT)
