from django.apps import AppConfig
class PyquizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PyQuiz'
    verbose_name="Python Quiz"

    class Meta:
        app_label = "PyQuiz"
    