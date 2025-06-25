from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, PatientViewSet, DoctorViewSet, PatientDoctorMappingViewSet, EmailTokenObtainPairView

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'mappings', PatientDoctorMappingViewSet, basename='mapping')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Custom route for GET /api/mappings/<patient_id>/
    path('mappings/<int:pk>/', PatientDoctorMappingViewSet.as_view({'get': 'by_patient'}), name='mapping-by-patient'),
    path('', include(router.urls)),
]
