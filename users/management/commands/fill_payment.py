from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        payment_for_create = []

        for user in User.objects.all():
            payment_for_create.append(Payment(user=user,
                                              lesson=Lesson.objects.get(pk=2),
                                              payment_amount=5000,
                                              payment_method='cash'))
        for user in User.objects.all():
            payment_for_create.append(Payment(user=user,
                                              course=Course.objects.get(pk=2),
                                              payment_amount=10000,
                                              payment_method='transfer'))

        Payment.objects.bulk_create(payment_for_create)
