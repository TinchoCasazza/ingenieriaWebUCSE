from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Grupo, Publicacion, Comentario, Evento, UserGrupos, Perfil
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PublicacionForm(ModelForm):
    class Meta:
        model = Publicacion
        widgets = {
            'foo': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
        }
        exclude = ['Publicado','Borrador','Estado','Destacar','idUserPublico','idGrupoPu' ]

class NuevoGrupo(ModelForm):
    class Meta:
        model = Grupo
        exclude = ['idGrupo','Creador','FechaCreacionG']

    def save(self, commit=True):
        self.instance.Creador = self.request.user
        return super().save(commit=commit)

class AdminGrupoForm(ModelForm):
    class Meta:
        model = UserGrupos
        exclude = ['idGrupoUsuario',]

class PrivacidadGrupoForm(ModelForm):
    class Meta:
        model = Grupo
        fields = ['NivelAcceso']

class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        widgets = {
            'foo': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
        }
        fields = ['ContenidoComentario']

class EditarPerfil(ModelForm):
    class Meta:
        model = Perfil
        exclude =  ['idPerfil']        

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class EventoForm(ModelForm):
    class Meta:
        model = Evento
        exclude = ['CreadorEvento','idGrupoEvento']
        widgets = {
            'FechaEvento': DateInput(format="%d/%m/%Y"),
            'Hora': TimeInput()
        }