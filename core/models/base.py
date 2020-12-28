from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)
