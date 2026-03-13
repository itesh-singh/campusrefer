from rest_framework import serializers
from accounts.models import User
from alumni.models import AlumniProfile
from students.models import StudentProfile
from connections.models import ConnectionRequest
from jobs.models import JobPost
from core.models import Notification


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class AlumniProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AlumniProfile
        fields = [
            "id", "user", "full_name", "batch_year", "branch",
            "current_company", "current_role", "city", "linkedin_url",
            "open_to_mentorship", "open_to_referrals", "is_verified",
            "bio", "profile_views",
        ]


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "id", "user", "full_name", "year", "branch",
            "skills", "target_role", "bio",
        ]


class ConnectionRequestSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    alumni = UserSerializer(read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = [
            "id", "student", "alumni", "request_type",
            "message", "status", "created_at",
        ]


class SendConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = ["request_type", "message"]


class JobPostSerializer(serializers.ModelSerializer):
    alumni = UserSerializer(read_only=True)

    class Meta:
        model = JobPost
        fields = [
            "id", "alumni", "title", "company", "location",
            "job_type", "description", "apply_link",
            "deadline", "is_active", "created_at",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "message", "is_read", "created_at"]