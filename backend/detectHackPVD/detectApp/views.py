from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import ViolationRecord
from .serializers import ViolationRecordSerializer
from django.utils import timezone

class ViolationRecordViewSet(viewsets.ModelViewSet):
    queryset = ViolationRecord.objects.all()
    serializer_class = ViolationRecordSerializer
    parser_classes = [MultiPartParser]  # для обработки видеофайлов

    # Штрафы по статьям
    FINE_DICT = {
        "Статья 12.12 часть 2 1. невыполнение требования ПДД об остановке перед стоп-линией, обозначенной дорожными знаками или разметкой проезжей части дороги, при запрещающем сигнале светофора или запрещающем жесте регулировщика": 800,
        "Статья 12.15 часть 4 Выезд в нарушение правил дорожного движения на полосу, предназначенную для встречного движения, при объезде препятствия, либо на трамвайные пути встречного направления, за исключением случаев, предусмотренных частью 3 настоящей статьи": 5000,
        "Статья 12.16. часть 1 Несоблюдение требований, предписанных дорожными знаками или разметкой проезжей части дороги": 500,
        "Статья 12.16 часть 2 Поворот налево или разворот в нарушение требований, предписанных дорожными знаками или разметкой проезжей части дороги": 1000,
        "Статья 12.17  часть 1.1 и 1.2. движение транспортных средств по полосе для маршрутных транспортных средств или остановка на указанной полосе в нарушение Правил дорожного движения ": 1500,
    }

    def create(self, request, *args, **kwargs):
        video_file = request.FILES.get('video')

        if not video_file:
            return Response({"error": "Видео не загружено."}, status=status.HTTP_400_BAD_REQUEST)

        # Сохранение видео
        violation_record = ViolationRecord(video=video_file)
        violation_record.save()

        # Обработка видео с помощью ML-модели
        # Предположим, что ML-модель возвращает данные о нарушении
        ml_model_result = self.process_video_with_ml_model(violation_record.video.path)

        # Определение штрафа на основе статьи
        fine_amount = self.get_fine_amount(ml_model_result["article"])

        # Заполнение полей модели
        violation_record.violation_article = ml_model_result["article"]
        violation_record.violation_time = ml_model_result["time"]
        violation_record.fine_amount = fine_amount
        violation_record.save()

        serializer = self.get_serializer(violation_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def process_video_with_ml_model(self, video_path):
        # Взаимодействие с ML-моделью
        # Замените это на фактический вызов ML-модели
        return {
            "article": "Статья 12.16. часть 1 Несоблюдение требований, предписанных дорожными знаками или разметкой проезжей части дороги",
            "time": 120
        }

    def get_fine_amount(self, article):
        # Возвращает штраф на основе словаря FINE_DICT
        return self.FINE_DICT.get(article, 0)
