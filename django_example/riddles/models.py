from django.db import models

# Create your models here.


class InputCommandsModel(models.Model):
    input_line = models.CharField(max_length=50)

class Progress_model(models.Model):
    username = models.CharField(max_length= 50, blank=True)
    score = models.IntegerField()
    kol_lessons = models.IntegerField()
    all_answers = models.IntegerField()
    good_answers = models.IntegerField()

    objects = models.Manager()#иначе выдает ошибку, где в views.py пишу objects

