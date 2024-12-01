from django.urls import path
from api.views import register, login_view, logout_view, flip_coin, shop_items, get_game_data, update_points, top_rankings, purchase_item

urlpatterns = [
    path("register", register, name="register"),              # 회원가입
    path("login", login_view, name="login"),                  # 로그인
    path("logout", logout_view, name="logout"),               # 로그아웃
    path("shop-items", shop_items, name="shop_items"),  # /api/shop-items
    path('flip-coin', flip_coin, name='flip_coin'),
    path('get-game-data/', get_game_data, name='get_game_data'),
    path('update-points/', update_points, name='update_points'),
    path("top-rankings", top_rankings, name="top_rankings"),
    path("purchase-item", purchase_item, name="purchase_item"),
]
