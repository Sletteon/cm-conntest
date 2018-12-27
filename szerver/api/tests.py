from django.test import TestCase
from .models import Bejegyzes
import datetime
import json
# Create your tests here.


class BejegyzesModelTests(TestCase):

    # Admin felületen mutatott név tesztejei
    # E heti bejegyzéssel
    def test_name_with_this_week(self):
        test_bejegyzes = Bejegyzes(uname='Test', het=datetime.date.today().isocalendar()[1], nap=0, tant='tant', anyag='anyag')
        self.assertIn('Ez a hét', test_bejegyzes.__str__())

    # Előző heti bejegyzéssel
    def test_name_with_last_week(self):
        test_bejegyzes = Bejegyzes(uname='Test', het=datetime.date.today().isocalendar()[1]-1, nap=0, tant='tant', anyag='anyag')
        self.assertIn('Múlt hét', test_bejegyzes.__str__())

    # Következő heti bejegyzéssel
    def test_name_with_next_week(self):
        test_bejegyzes = Bejegyzes(uname='Test', het=datetime.date.today().isocalendar()[1]+1, nap=0, tant='tant', anyag='anyag')
        self.assertIn('Következő', test_bejegyzes.__str__())

    # Nem előző és nem következő (számozott) heti bejegyzéssel
    def test_name_with_numbered_week(self):
        test_bejegyzes = Bejegyzes(uname='Test', het=datetime.date.today().isocalendar()[1]-2, nap=0, tant='tant', anyag='anyag')
        self.assertIn(str(datetime.date.today().isocalendar()[1]-2), test_bejegyzes.__str__())


# API hívások tesztjei
class TestCalls(TestCase):

    def create_bejegyzes(self, week_number=datetime.date.today().isocalendar()[1], return_dict=False):
        sending_dict = {"uname": "test", "het": week_number, "nap": datetime.datetime.now().weekday(), "tant": "test", "anyag": "test"}
        self.client.post('', sending_dict, follow=True)

        if return_dict:
            return sending_dict

    # beküldést és lehívást tesztel
    def test_view_getting_and_setting_data(self):
        sending_dict = self.create_bejegyzes(return_dict=True)
        response = self.client.get('')

        [self.assertContains(response, i) for i in sending_dict]

    # csak egy heti lehívás, ki kell szűrnie a kettő bejegyzésből ez erre a hétre szólót
    def test_view_getting_only_this_week(self):
        week_number = datetime.date.today().isocalendar()[1]
        self.create_bejegyzes(week_number=week_number)
        self.create_bejegyzes(week_number=week_number+1)
        self.create_bejegyzes(week_number=week_number-1)
        self.create_bejegyzes(week_number=week_number+234)
        response = self.client.get('/het/' + str(week_number) + '/')

        self.assertEqual(len(json.loads(response.content)), 1)

    # bejegyzés törlése
    def test_view_deleting(self):
        self.create_bejegyzes()
        response = self.client.get('')
        self.client.delete('/delete/' + str(json.loads(response.content)[0]['id']) + '/')
        response = self.client.get('')
        self.assertEqual(json.loads(response.content), [])
