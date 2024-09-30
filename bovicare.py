usuarios/models.py:
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Campos adicionais específicos para o BoviCare
    nome_usuario = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    senha = models.CharField(max_length=128)
    primeiro_nome = models.CharField(max_length=150, blank=True, null=True)
    sobrenome = models.CharField(max_length=150, blank=True, null=True)
    eh_funcionario = models.BooleanField(default=False)
    eh_ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    nome_fazenda = models.CharField(max_length=100, blank=True, null=True)
    funcao = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'nome_usuario'
    REQUIRED_FIELDS = ['email']

    def _str_(self):
        return self.nome_usuario
usuarios/serializers.py:

from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome_usuario', 'email', 'primeiro_nome', 'sobrenome', 'eh_funcionario', 'eh_ativo', 'data_cadastro', 'nome_fazenda', 'funcao', 'senha']
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user
usuarios/views.py:

from rest_framework import viewsets
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
usuarios/urls.py:

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
Atualize o settings.py:

INSTALLED_APPS = [
    # outros apps
    'rest_framework',
    'rest_framework_simplejwt',
    'usuarios',  # O app de usuários
    'gado',  # O app de gado
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
usuarios/urls.py (Login JWT):
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
gado/models.py:
python
Copiar código
from django.db import models

class Gado(models.Model):
    numero_brinco = models.CharField(max_length=50, unique=True)
    raca = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    estado_saude = models.CharField(max_length=50)
    ultima_verificacao = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.numero_brinco
gado/serializers.py:
python
Copiar código
from rest_framework import serializers
from .models import Gado

class GadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gado
        fields = '_all_'

gado/views.py:
from rest_framework import generics
from .models import Gado
from .serializers import GadoSerializer

class GadoListView(generics.ListAPIView):
    queryset = Gado.objects.all()
    serializer_class = GadoSerializer

gado/urls.py:
from django.urls import path
from .views import GadoListView

urlpatterns = [
    path('gado/', GadoListView.as_view(), name='gado_list'),
]

Arquivo bovicare/urls.py:
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),  # Endpoints de usuários e login
    path('api/', include('gado.urls')),  # Endpoints de gado
]
