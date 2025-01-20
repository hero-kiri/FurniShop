from django.db import models


class Category(models.Model):
    """
    Модель категории для классификации мебели.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание категории")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Furniture(models.Model):
    """
    Модель мебели.
    """
    name = models.CharField(max_length=255, verbose_name="Название мебели")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="furniture", verbose_name="Категория"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество в наличии")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to="furniture_images/", blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Мебель"
        verbose_name_plural = "Мебель"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class FurnitureDetail(models.Model):
    """
    Модель для подробного описания мебели.
    """
    furniture = models.OneToOneField(
        'Furniture', on_delete=models.CASCADE, related_name='detail', verbose_name="Мебель"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    material = models.CharField(max_length=255, blank=True, null=True, verbose_name="Материал")
    color = models.CharField(max_length=100, blank=True, null=True, verbose_name="Цвет")
    dimensions = models.CharField(max_length=100, blank=True, null=True, verbose_name="Размеры (ДxШxВ)")
    weight = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Вес (кг)")
    manufacturer = models.CharField(max_length=255, blank=True, null=True, verbose_name="Производитель")
    warranty_period = models.CharField(max_length=100, blank=True, null=True, verbose_name="Гарантийный срок")
    care_instructions = models.TextField(blank=True, null=True, verbose_name="Инструкции по уходу")
    additional_features = models.TextField(blank=True, null=True, verbose_name="Дополнительные функции")

    class Meta:
        verbose_name = "Описание мебели"
        verbose_name_plural = "Описание мебели"

    def __str__(self):
        return f"Описание для {self.furniture.name}"

