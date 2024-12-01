from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from .models import Game, Ranking, Item, CustomUser, CustomToken, UserItem
from .serializers import ItemSerializer, GameSerializer, RankingSerializer
from django.utils.crypto import get_random_string
import random


# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # 필수 필드 확인
    if not username or not email or not password:
        return Response({"message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    # 중복 사용자 확인
    if CustomUser.objects.filter(username=username).exists():
        return Response({"message": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(email=email).exists():
        return Response({"message": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

    # 사용자 생성
    user = CustomUser.objects.create(
        username=username,
        email=email,
        password=make_password(password)  # 비밀번호 암호화
    )

    return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        data = request.data
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return Response({"message": "Email and password are required."}, status=400)

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({"message": "User not found."}, status=404)

        auth_user = authenticate(username=user.username, password=password)
        if auth_user is not None:
            login(request, auth_user)

            # 기존 토큰 삭제
            CustomToken.objects.filter(user=auth_user).delete()

            # 새로운 토큰 생성
            token = CustomToken.objects.create(
                user=auth_user,
                key=get_random_string(40)
            )

            return Response({
                "message": "Login successful.",
                "user": {
                    "username": auth_user.username,
                    "email": auth_user.email,
                },
                "token": token.key,  # 새로운 토큰 반환
            }, status=200)
        else:
            return Response({"message": "Invalid credentials."}, status=400)

    except Exception as e:
        print(f"Error: {e}")
        return Response({"message": "An error occurred.", "error": str(e)}, status=500)
    
# 로그아웃
@api_view(['POST'])
def logout_view(request):
    try:
        # 세션 로그아웃
        logout(request)

        # 토큰 삭제 (토큰 인증 사용 시)
        if hasattr(request.user, 'auth_token_custom'):
            request.user.auth_token_custom.delete()


        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "An error occurred during logout.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 동전 던지기
@api_view(['POST'])
def flip_coin(request):
    user = request.user
    print("flip_coin view called") 
    # 사용자 인증 확인
    if not user.is_authenticated:
        return Response({"message": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # 동전 던지기 성공 확률 계산 (CustomUser의 메서드 사용)
        probability = user.get_success_probability()

        # 동전 던지기 결과 계산
        is_heads = random.randint(1, 100) <= probability  # 성공 여부 판정
        result = "HEADS" if is_heads else "TAILS"
        earned_points = 1 if is_heads else 0  # 성공 시 1점 추가

        # Game 테이블에 결과 저장
        game = Game.objects.create(
            user=user,
            result=result,
            earned_points=earned_points
        )

        # Ranking 테이블 업데이트
        ranking, created = Ranking.objects.get_or_create(user=user)
        ranking.points += earned_points
        ranking.save()

        # 직렬화를 사용하여 데이터 변환
        game_serializer = GameSerializer(game)
        ranking_serializer = RankingSerializer(ranking)

        return Response({
            "message": "Coin flipped successfully.",
            "result": game_serializer.data,
            "ranking": ranking_serializer.data,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": "An error occurred during the game.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def get_game_data(request):
    print(f"Authorization Header: {request.headers.get('Authorization')}")
    print(f"User: {request.user}, Is Authenticated: {request.user.is_authenticated}")

    user = request.user
    if not user.is_authenticated:
        return Response({"message": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        probability = user.get_success_probability()
        ranking, created = Ranking.objects.get_or_create(user=user)

        return Response({
            "message": "Game data retrieved successfully.",
            "probability": probability,
            "ranking": {
                "points": ranking.points,
                "last_updated": ranking.last_updated,
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error: {e}")
        return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def update_points(request):
    user = request.user
    print("update_points view called")

    # 사용자 인증 확인
    if not user.is_authenticated:
        return Response({"message": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # 추가할 포인트를 요청 데이터에서 가져옴
        points_to_add = request.data.get("points", 0)
        if not isinstance(points_to_add, int) or points_to_add <= 0:
            return Response({"message": "Invalid points value. Must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Ranking 테이블에서 사용자 데이터 가져오기 (없으면 생성)
        ranking, _ = Ranking.objects.get_or_create(user=user)

        # 포인트 업데이트
        ranking.points += points_to_add
        ranking.save()

        # 직렬화를 사용하여 데이터 변환
        ranking_serializer = RankingSerializer(ranking)

        return Response({
            "message": "Points updated successfully.",
            "updated_ranking": ranking_serializer.data,  # 직렬화된 사용자 랭킹 데이터 반환
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"message": "An error occurred while updating points.", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def shop_items(request):
    try:
        items = Item.objects.all()  # 모든 아이템 가져오기
        serializer = ItemSerializer(items, many=True)  # 직렬화
        return Response({"items": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"message": "Failed to load items.", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(['POST'])
def purchase_item(request):
    user = request.user
    item_id = request.data.get("item_id")
    
    try:
        item = Item.objects.get(id=item_id)
        user_item, created = UserItem.objects.get_or_create(
            user=user,
            item=item,
            defaults={"quantity": 1, "current_price": item.base_price},
        )
        if not created:
            # Increase quantity and adjust current price
            user_item.quantity = F('quantity') + 1
            user_item.current_price += 10  # Increase price by 10 per quantity
            user_item.save()
            user_item.refresh_from_db()  # Reload updated values

        return Response(
            {"message": f"Successfully purchased {item.name}.", "quantity": user_item.quantity},
            status=status.HTTP_200_OK,
        )
    except Item.DoesNotExist:
        return Response(
            {"message": "Item not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"message": "Failed to purchase item.", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
@api_view(['POST'])
@permission_classes([AllowAny])
def top_rankings(request):
    # Fetch top 10 players ordered by points
    top_players = Ranking.objects.order_by('points')[:10]
    rankings = [
        {
            "id": player.user_id,
            "points": player.points
        }
        for player in top_players
    ]
    return Response({"rankings": rankings})