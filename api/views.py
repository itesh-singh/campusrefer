from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from accounts.models import User
from alumni.models import AlumniProfile
from connections.models import ConnectionRequest
from core.models import Notification
from core.utils import create_notification
from jobs.models import JobPost

from .serializers import (
    AlumniProfileSerializer,
    ConnectionRequestSerializer,
    JobPostSerializer,
    NotificationSerializer,
    RegisterSerializer,
    SendConnectionRequestSerializer,
    StudentProfileSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class AlumniListView(generics.ListAPIView):
    serializer_class = AlumniProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AlumniProfile.objects.select_related("user").all()
        company = self.request.query_params.get("company")
        city = self.request.query_params.get("city")
        branch = self.request.query_params.get("branch")
        mentorship = self.request.query_params.get("mentorship")
        referral = self.request.query_params.get("referral")
        q = self.request.query_params.get("q")

        if q:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(full_name__icontains=q) |
                Q(current_company__icontains=q) |
                Q(current_role__icontains=q) |
                Q(city__icontains=q)
            )
        if company:
            queryset = queryset.filter(current_company__icontains=company)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if branch:
            queryset = queryset.filter(branch__icontains=branch)
        if mentorship == "yes":
            queryset = queryset.filter(open_to_mentorship=True)
        if referral == "yes":
            queryset = queryset.filter(open_to_referrals=True)

        return queryset


class AlumniDetailView(generics.RetrieveAPIView):
    serializer_class = AlumniProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = AlumniProfile.objects.select_related("user").all()


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "student":
            profile = get_object_or_404(
                request.user.__class__,
                pk=request.user.pk
            )
            serializer = StudentProfileSerializer(
                request.user.student_profile
            )
        else:
            serializer = AlumniProfileSerializer(
                request.user.alumni_profile
            )
        return Response(serializer.data)


class JobListView(generics.ListAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]
    queryset = JobPost.objects.filter(is_active=True).select_related("alumni")


class JobDetailView(generics.RetrieveAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]
    queryset = JobPost.objects.select_related("alumni").all()


class ConnectionListView(generics.ListAPIView):
    serializer_class = ConnectionRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return ConnectionRequest.objects.filter(
                student=user
            ).select_related("student", "alumni")
        return ConnectionRequest.objects.filter(
            alumni=user
        ).select_related("student", "alumni")


class SendConnectionRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, alumni_id):
        if request.user.role != "student":
            return Response(
                {"error": "Only students can send requests."},
                status=status.HTTP_403_FORBIDDEN,
            )

        alumni_user = get_object_or_404(
            User, id=alumni_id, role=User.Roles.ALUMNI
        )

        existing = ConnectionRequest.objects.filter(
            student=request.user, alumni=alumni_user
        ).exists()

        if existing:
            return Response(
                {"error": "Request already sent."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SendConnectionRequestSerializer(data=request.data)
        if serializer.is_valid():
            conn = serializer.save(
                student=request.user,
                alumni=alumni_user,
            )
            create_notification(
                user=alumni_user,
                message=f"{request.user.username} sent you a {conn.request_type} request.",
            )
            return Response(
                ConnectionRequestSerializer(conn).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)