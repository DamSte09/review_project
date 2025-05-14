from django.db import models


class Review(models.Model):
    text = models.TextField(max_length=200)
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]