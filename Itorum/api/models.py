from django.db import models


class Order(models.Model):
    """ Модель с заказом """
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='epson_sessions',
                             verbose_name='Заказчик')
    total = models.FloatField(null=True, blank=False, default=0, max_length=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время заказа')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ-{self.pk}'


class Customer(models.Model):
    """ Модель заказчика """
    name = models.CharField('Имя заказчика', blank=False, max_length=256, unique=True)

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    def __str__(self):
        return f'Заказчик-{self.name}'


