from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser  # Django 기본 User 모델 사용 가능
from django.utils.timezone import now

    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # 이메일은 고유해야 함
    psw = models.CharField(max_length=255)  # 비밀번호 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 계정 생성 시간

    def __str__(self):
        return self.username
    
    def get_success_probability(self):
        # 플레이어의 아이템 보유 상태 기반 성공 확률 계산
        base_probability = 50  # 기본 확률
        bonus_probability = sum(
            item.quantity  # 아이템 효과 계산
            for item in self.user_items.all()
        )
        return (base_probability + bonus_probability)
    
class CustomToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(
        CustomUser,
        related_name='auth_token',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
        db_table = "api_customtoken"  # 테이블 이름 명시

# Games 테이블
class Game(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 유저 ID (Foreign Key)
    result = models.CharField(max_length=10, choices=[('HEADS', 'Heads'), ('TAILS', 'Tails')])  # 결과
    earned_points = models.IntegerField()  # 획득한 포인트
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"{self.user.username} - {self.result} - {self.earned_points}"

# Items 테이블
class Item(models.Model):
    name = models.CharField(max_length=50)  # 아이템 이름
    base_price = models.IntegerField()  # 기본 가격
    description = models.TextField()  # 설명

    def __str__(self):
        return self.name

# User_Items 테이블
class UserItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_items')  # related_name 추가
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # 아이템 ID
    quantity = models.IntegerField(default=0)  # 아이템 수량
    current_price = models.IntegerField()  # 현재 가격

    @property
    def probability_increase(self):
        return self.quantity  # 1% probability per quantity

    def __str__(self):
        return f"{self.user.username} - {self.item.name} ({self.quantity})"

# Logs 테이블
class Log(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Friends 테이블
class Friend(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendships')  # 주체 유저 ID
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends')  # 친구 유저 ID
    created_at = models.DateTimeField(auto_now_add=True)  # 친구 추가 시간

    class Meta:
        unique_together = ('user', 'friend')  # 동일한 친구 관계 중복 방지

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"

# Rankings 테이블
class Ranking(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.points} points"

