from rest_framework.generics import ListAPIView, ListCreateAPIView, DestroyAPIView
from django.views import View
from django.http import HttpResponse
from .models import Bejegyzes
from .serializers import BejegyzesSerializer

# Create your views here.


class BejegyzesekList(ListCreateAPIView):
    queryset = Bejegyzes.objects.all()
    serializer_class = BejegyzesSerializer


class EHetiBejegyzesek(ListAPIView):
    serializer_class = BejegyzesSerializer

    def get_queryset(self):
        return Bejegyzes.objects.filter(het=self.kwargs['het'])


class BejegyzesekTorlese(DestroyAPIView):
    serializer_class = BejegyzesSerializer

    def get_queryset(self):
        return Bejegyzes.objects.filter(id=self.kwargs['pk'])


class motd(View):
    def get(self, request):
        return HttpResponse('alsjdfhalsdkjf')
