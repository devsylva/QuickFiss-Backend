from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsArtisan, IsClient
from accounts.models import ClientProfile, ArtisanProfile
from core.models import Post, Category, Service
from .serializers import CategorySerializer, ServiceSerializer

# Create your views here.
class ClientPersonalizedFeed(APIView):
    permission_classes = [IsAuthenticated]

    def get(request):
        user = request.user
        post = Post.objects.order_by('-created_at')

        profile = ClientProfile.objects.get(user=user)
        preferred_categories = profile.preferred_categories.all()
        followed_tags = profile.followed_tags.all()

        # query to get clients preferred services for personalized experience
        posts = Post.objects.filter(
            Q(category__in=preferred_categories) | Q(tags__in=followed_tags)
        ).distinct()

        # Boost posts based on interactions
        liked_post = UserInteraction.objects.filter(
            user=user, liked=True
        ).values_list('post_id', flat=True)
        posts = posts.order_by(
            models.Case(
                models.When(id__in=liked_posts, then=0),  # Prioritize liked posts
                default=1,
                output_field=models.IntegerField()
            ),
            '-created_at'  # Then sort by recency
        )[:20]

        return Response(posts, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    permission = [IsAuthenticated,]

    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({
                "mesage": "Categories retrieved successfully",
                "data": serializer.data
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": f"failed to retrieve categories {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceListView(APIView):
    permission = [IsAuthenticated]

    def get(self, request):
        try:

            category = request.query_params.get('category', None)
            services = Service.objects.all()

            if category:
                if not Category.objects.filter(name=category).exists():
                    return Response({
                        "error": f"category '{category}' does not exist"
                    }, status=status.HTTP_400_BAD_REQUEST)
                services  = Service.objects.filter(category__name=category)


            serializer = ServiceSerializer(services, many=True)
            return Response({
                "message": "Services retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"failed to retrieve services {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)