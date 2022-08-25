from django.db import models
# ユーザー認証
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator

# ユーザーアカウントのモデルクラス
class Account(models.Model):

    # ユーザー認証のインスタンス(1vs1関係)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 追加フィールド
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    account_image = models.ImageField(upload_to="profile_pics",blank=True)
    private_mac_adress = models.CharField(max_length=12, validators=[MinLengthValidator(12),RegexValidator(r'^[A-Z0-9]*$')])
    kotei_mac_adress = models.CharField(max_length=12, validators=[MinLengthValidator(12),RegexValidator(r'^[A-Z0-9]*$')])
    zaisitu_state = models.CharField(max_length=10)
    syusseki_state = models.CharField(max_length=10)
    syusseki_Nissu = models.CharField(default=0,max_length=10)
   
    def __str__(self):
        return self.user.username

class MAC(models.Model):
    mac =  models.CharField(max_length=100)
    mac2 = models.CharField(max_length=100)

    def __str__(self):
        return self.mac

class MACsikibetu(models.Model):
    mac_s =  models.CharField(max_length=100)
    mac2 = models.CharField(max_length=100)

    def __str__(self):
        return self.mac_s