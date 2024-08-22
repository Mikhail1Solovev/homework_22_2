from django.db import models
from django.conf import settings

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, default='Uncategorized')
    is_published = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_owner')  # Владелец продукта

    class Meta:
        permissions = [
            ("can_unpublish_product", "Может отменить публикацию продукта"),
            ("can_change_product_description", "Может менять описание любого продукта"),
            ("can_change_product_category", "Может менять категорию любого продукта"),
        ]

    def __str__(self):
        return self.title
