from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(verbose_name='Название категории', max_length=100)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(max_length=200, verbose_name='Название продукта')
    price = models.FloatField(verbose_name='Цена продукта')
    description = models.TextField(blank=True, null=True, verbose_name='Описание продукта')
    rating = models.FloatField(verbose_name="Рейтинг продукта", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    link = models.URLField(verbose_name="Ссылка на Amazon")
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='Категория')

    def __str__(self):
        return f'{self.name}, {self.category}'


class ProductImage(models.Model):
    class Meta:
        verbose_name = 'Картинка продукта'
        verbose_name_plural = 'Картинки продукта'

    src = models.ImageField(upload_to='images/products', verbose_name='Картинки')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Продукт',
                                related_name='images',
                                blank=True,
                                null=True)

    def __str__(self):
        return f'Картинка {self.product.name}'


class UserPersonalCart(models.Model):
    class Meta:
        verbose_name = 'Корзина пользователя'

    owner = models.OneToOneField(User,
                                 on_delete=models.CASCADE,
                                 verbose_name='Владелец корзины',
                                 related_name='cart',
                                 blank=True,
                                 null=True)

    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total


class CartItem(models.Model):
    class Meta:
        verbose_name = 'Запись корзины'
        verbose_name_plural = 'Записи корзины'

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='carts',
                                verbose_name='Продукт')
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(UserPersonalCart,
                             on_delete=models.CASCADE,
                             related_name='items',
                             verbose_name='Корзина',
                             blank=True,
                             null=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(auto_now_add=True)
    phone_number = models.CharField(blank=True, null=True, max_length=20)
    location = models.CharField(max_length=150)

    @receiver(post_save, sender=User)
    def create_user_personal_cart(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            UserPersonalCart.objects.create(owner=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
