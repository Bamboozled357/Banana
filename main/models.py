from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# статусы: (открытый, закрытый, черновик)
"""каждый вариант выбора представляется в виде tuple(кортежа) из двух элементов:
(ключ, текст) где ключ хранится в БД, а текст используется  для отображения"""
STATUS_CHOICES = (
    ('open', 'Открытое'),
    ('closed', 'Закрытое'),
    ('draft', 'Черновик')
)


class Publication(models.Model):
    """Классы, которые наследуются от models.Model являются моделями, то есть
    отвечают за связь с БД через ORM, в БД будет создана таблица с указанными
    полями"""
    title = models.CharField('Заголовок', max_length=255)
    # CharField - VARCHAR(), обязательное свойство max_length
    text = models.TextField('Текст')
    # TextField - TEXT
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES)
    """choices - жёстко ограниченные варианты выбора, т.е никакие иные значения 
    не принимаются"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='pubs', verbose_name='Автор')
    """ForeignKey - поле для связи с другой моделью, обязательные свойства: модель,
    on_delete - определяет, что произойдёт с объявлением, если удалить автора из БД"""
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    """DateTimeField - TIMESTAMP in SQL, auto_now_add - время задаётся при добавлении записи,
    auto_now - время задаётся при изменении записи"""
    updated_at = models.DateTimeField('Дата редактирования', auto_now=True)

    class Meta:
        verbose_name = 'Объявления'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class Comment(models.Model):
    publication = models.ForeignKey(Publication,
                                    on_delete=models.CASCADE,
                                    related_name='comments', verbose_name='Публикация')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Автор')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.publication} --> {self.user}'