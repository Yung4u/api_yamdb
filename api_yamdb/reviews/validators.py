from datetime import datetime

from rest_framework import serializers


def validate_year(data):
    if data >= datetime.now().year:
        raise serializers.ValidationError(
            message='Укажите правильный год',
            params={'data': data},
        )
