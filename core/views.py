from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegisterSerializer, PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers

# User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

# Patient Views
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Doctor Views
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

# Patient-Doctor Mapping Views
class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mapping = PatientDoctorMapping.objects.create(
            patient=serializer.validated_data['patient'],
            doctor=serializer.validated_data['doctor']
        )
        output_serializer = self.get_serializer(mapping)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            return PatientDoctorMapping.objects.filter(patient_id=patient_id)
        return super().get_queryset()

    @action(detail=True, methods=['get'], url_path='', url_name='by_patient')
    def by_patient(self, request, pk=None):
        """Get all mappings for a specific patient by patient_id in the URL."""
        mappings = PatientDoctorMapping.objects.filter(patient_id=pk)
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)

# Custom JWT Login Serializer and View
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        self.fields['email'] = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            users = User.objects.filter(email=email)
            if not users.exists():
                raise serializers.ValidationError('No user with this email.')
            elif users.count() > 1:
                raise serializers.ValidationError('Multiple users with this email, please contact admin.')

            user = users.first()
            if user:
                attrs['username'] = user.username
        else:
            raise serializers.ValidationError('Email and password are required.')
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    class Meta:
        fields = ('email', 'password')

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
