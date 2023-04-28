from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

        #lipiar el campo email
    def clean_email(self):
        email = self.cleaned_data('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'El email ya esta registrado, prueba con otro.')
        
        return email
        

    #modificamos el método save() así podemos definir  user.is_active a False la primera vez que se registra
    def save(self, commit=True):        
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False # No está activo hasta que active el vínculo de verificación
            user.save()

        return user
