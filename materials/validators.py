import re
from rest_framework.serializers import ValidationError


class ValidatorYoutubeLink:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = r'^https://www.youtube.com/watch\?v='
        tmp = dict(value).get(self.field)
        result = re.match(pattern, tmp)
        if not result:
            raise ValidationError('Не допустимая ссылка!')
