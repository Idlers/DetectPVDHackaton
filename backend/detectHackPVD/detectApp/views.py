import openpyxl
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
        saved_records=[]
        for result in ml_model_result:
            article = result["article"]
            time = result["time"]

            # Определяем штраф на основе статьи
            fine_amount = self.get_fine_amount(article)

            # Создаем и сохраняем запись для каждого нарушения
            violation_record = ViolationRecord(
                video=video_file,
                violation_article=article,
                violation_time=time,
                fine_amount=fine_amount
            )
            violation_record.save()
            saved_records.append(violation_record)


        serializer = self.get_serializer(saved_records, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def process_video_with_ml_model(self, video_path):
        # Взаимодействие с ML-моделью
        file_path = 'result/result.xlsx' #здесь должен происходить вызов ml-модели, которая вернет путь к сохраненному excel
        # Открываем Excel файл
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        violations_data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            violation_article = row[1]
            violation_time = row[2]
            if violation_time is not None:
                violations_data.append({
                    "article": violation_article,
                    "time": int(violation_time)
                })
                print(violations_data)


        return violations_data

    def get_fine_amount(self, article):
        # Возвращает штраф на основе словаря FINE_DICT
        print(self.FINE_DICT.get(article, 0))
        return self.FINE_DICT.get(article, 0)
