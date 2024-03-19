from django.shortcuts import render
from django.views import View
# from .models import ...


class TrainView(View):
    def get(self, request):
        context = {}  # Создайте здесь запросы к БД
        return render(request, 'train_db/training_db.html', context=context)

