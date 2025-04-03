import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from apps.db_train_alternative.models import Blog, Author, AuthorProfile, Entry, Tag

    # TODO Сделайте здесь запросы

    # obj = Entry.objects.filter(author__name__contains='author')
    # print(obj)

obj = Entry.objects.filter(author__name__contains='author')
print(obj)
"""<QuerySet [<Entry: Оазисы Сахары: красота и опасность>, 
<Entry: Новые гаджеты и устройства: обзор рынка>]>"""
obj = Entry.objects.filter(author__authorprofile__city=None)
print(obj)











