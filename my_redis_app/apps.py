from django.apps import AppConfig


class MyRedisAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_redis_app'
