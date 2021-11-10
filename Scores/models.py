from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model() 



class Scores(models.Model):
    player = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField()
    Score = models.IntegerField()

    def __str__(self):
        return self.player.email


class Winners(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    did_win = models.BooleanField(default=True)