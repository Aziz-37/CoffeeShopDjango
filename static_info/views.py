from rest_framework.views import APIView
from rest_framework.response import Response

class StaticInfoView(APIView):
    permission_classes = []

    def get(self, request):
        data = {
            "location": "г. Ташкент, ул. Садыка Азимова, 1",
            "schedule": "Пн-Пт: 08:00-20:00, Сб-Вс: 10:00-18:00",
            "contact": "+998 71 220 02 02"
        }
        return Response(data)
