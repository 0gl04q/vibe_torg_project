from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4


class ActiveBuyerManager(models.Manager):
    """ Менеджер активных покупателей """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Buyer(models.Model):
    """ Модель покупателя """

    active = ActiveBuyerManager()
    objects = models.Manager()

    tg_id = models.BigIntegerField(verbose_name="Телеграмм ID", primary_key=True)
    nickname = models.CharField(max_length=64, verbose_name="Никнейм")

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('is_active',)

        indexes = [
            models.Index(fields=['tg_id', 'is_active']),
            models.Index(fields=['is_active'])
        ]

        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return self.nickname


class Order(models.Model):
    """ Модель заказа """

    class Status(models.TextChoices):
        PENDING = "PE", "В ожидании"
        IN_PROGRESS = "IP", "Ждем ответ"
        BY_AGREEMENT = "BA", "На согласовании"
        PAYED = "PA", "Оплачено"
        COMPLETED = "CO", "Выполнен"
        CANCELLED = "CA", "Отменен"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, verbose_name="Покупатель", related_name="orders")

    link = models.URLField(max_length=1000, verbose_name='Ссылка')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена товара", default=0)

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING, verbose_name='Статус')

    created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    class Meta:
        ordering = ('-created',)

        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['buyer'])
        ]

        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Message(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name="Заказ")
    getter = models.ForeignKey(Buyer, on_delete=models.PROTECT, verbose_name="Получатель")
    sender = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Отправитель")
