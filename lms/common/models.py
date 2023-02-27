from django.db import models


class DateBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-modified',)

    @property
    def created_date(self):
        return self.created.date()
