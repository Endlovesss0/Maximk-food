from django.contrib.auth.models import User
from django.db import models


class UserAdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="additional_info",
                                verbose_name="Пользователь")
    avatar = models.ImageField(verbose_name="Аватар", blank=True, null=True)
    about = models.TextField(verbose_name="О себе", blank=True, null=True)
    date_of_birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    place = models.CharField(max_length=150, verbose_name="Место проживания", blank=True, null=True)

    def __str__(self):
        return f"Дополнительные сведения о пользователе {self.user}"

    class Meta:
        verbose_name = "Дополнительные сведения о пользователе"
        verbose_name_plural = "Дополнительные сведения о пользователях"
