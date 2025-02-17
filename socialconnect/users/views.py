from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Follow
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer




class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token),
                "redirect": "http://localhost:3000"
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                refresh_token = RefreshToken.for_user(user)
                return Response({
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token),
                    "redirect": "http://localhost:3000"
                },status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
            
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,user_name):
        try:
            if user_name:
                user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
    def patch(self, request, user_name):
        try:
            user = User.objects.get(username=user_name)
            data = request.data
            if 'username' in data:
                return Response({'error': 'Cannot change username'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, user_name):
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # Blacklist all tokens associated with the user
        user.user_deactivate()
        
        return Response({"message":"User deactivated"}, status=status.HTTP_204_NO_CONTENT)
    
class SearchUsersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.query_params.get('q')
        users = User.objects.all()
        if query:
            users = users.filter(username__icontains=query)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, user_name):
        try:
            user_to_follow = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == user_to_follow:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)

        if created:
            return Response({'message': f'You are now following {user_to_follow.username}'}, status=status.HTTP_201_CREATED)
        return Response({'message': f'You are already following {user_to_follow.username}'}, status=status.HTTP_200_OK)
    

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, user_name):
        try:
            user_to_unfollow = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            follow = Follow.objects.get(follower=request.user, followed=user_to_unfollow)
            follow.delete()
            return Response({'message': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({'message': f'You are not following {user_to_unfollow.username}'}, status=status.HTTP_400_BAD_REQUEST)
