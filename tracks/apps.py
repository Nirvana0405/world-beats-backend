from django.apps import AppConfig


class TracksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracks'




from django.apps import AppConfig

class TracksConfig(AppConfig):
    name = 'tracks'  # ← 正しいアプリ名になっているか？
