from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, Doctor, PatientDoctorMapping

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate_phone(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient', write_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), source='doctor', write_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'doctor', 'patient_id', 'doctor_id', 'assigned_at')
        read_only_fields = ('assigned_at',)
