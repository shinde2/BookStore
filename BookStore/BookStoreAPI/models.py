from django.db import models
from django.contrib.auth.models import User


class BookCategory(models.Model):
    title = models.CharField(max_length=255, db_index=True, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"


class BookItem(models.Model):
    title = models.CharField(max_length=255, db_index=True, unique=True)
    author = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    book_category = models.ForeignKey(BookCategory, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title}"


class Cart(models.Model):
    bookitem = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.bookitem.title} - {self.user.username}"

    class Meta:
        unique_together = ["bookitem", "user"]


class Order(models.Model):
    status = models.IntegerField(default=0, db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="u")
    carrier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="c")

    def __str__(self):
        return f"{self.user.username}-{self.id}"


class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    bookitem = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.bookitem.title} - {self.order.user.username}"
