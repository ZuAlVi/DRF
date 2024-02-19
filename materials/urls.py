from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter
from django.urls import path

from materials import views


app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'course', views.CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', views.LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', views.LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', views.LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('courses/subscription/<int:pk>/', views.SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('courses/unsubscribe/<int:pk>/', views.SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),
    path('courses/buy/<int:pk>/', views.PaymentCreateAPIView.as_view(), name='buy_course'),
] + router.urls
