from django.db import models

from polymorphic.models import PolymorphicModel


class Log(models.Model):
    text = models.TextField()


class Entry(PolymorphicModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class EntryWithSignalFirst(Entry):
    pass


class EntryWithSignalForloop(Entry):
    pass


class EntryWithoutSignal(Entry):
    pass


class EntryWithSignalBrackets(Entry):
    pass
