from django.db import models
import datetime
import calendar
import locale

# Create your models here.


class Bejegyzes(models.Model):
    uname = models.CharField(max_length=120)
    het = models.IntegerField(default=datetime.date.today().isocalendar()[1])
    nap = models.IntegerField(default=datetime.datetime.today().weekday())
    tant = models.CharField(max_length=120)
    anyag = models.CharField(max_length=120)
    pic = models.TextField(max_length=10000, blank=True, null=True)

    # mi jelenjen meg pl. az admin felületen
    def __str__(self):
        # állítsa be, hogy a napok a rendszer nyelvén jelenjenek meg (jóesetben magyar)
        locale.setlocale(locale.LC_ALL, '')
        bejegyzes_name = ''

        # derítse ki, melyik héten lett beírva a bejegyzés, preferálja az írott formát a szám helyett
        if datetime.date.today().isocalendar()[1] == self.het:
            bejegyzes_name += 'Ez a hét '

        elif abs(datetime.date.today().isocalendar()[1] - self.het) == 1 and datetime.date.today().isocalendar()[1] > self.het:
            bejegyzes_name += 'Múlt hét '

        elif abs(datetime.date.today().isocalendar()[1] - self.het) == 1 and datetime.date.today().isocalendar()[1] < self.het:
            bejegyzes_name += 'Jövő hét '

        else:
            bejegyzes_name += str(self.het) + '. hét '

        # adja hozzá a meglévő stringhez a nap nevét 'i' vel a végén
        bejegyzes_name += str(list(calendar.day_name)[self.nap]) + 'i '
        # adja hozzá a lánchoz a tantárgy nevét kisbetűvel
        bejegyzes_name += str(self.tant).lower()

        return bejegyzes_name

    class Meta:
        verbose_name = 'bejegyzés'
        verbose_name_plural = 'bejegyzések'
