from django import forms

class reg_form(forms.Form):
    login = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'login', 'id': 'reg_1', 'class': 'fonts_fix'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'password', 'id': 'reg_2', 'class': 'fonts_fix'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'email', 'id': 'reg_3', 'class': 'fonts_fix'}))

class log_form(forms.Form):
    log_login = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'login', 'id': 'log_1', 'class': 'fonts_fix'}))
    log_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'password', 'id': 'log_2', 'class': 'fonts_fix'}))

class ip_form(forms.Form):
    ip_ip = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'ip', 'id': 'ip_3', 'class': 'fonts_fix'}))
    ip_user = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'name', 'id': 'ip_1', 'class': 'fonts_fix'}))
    ip_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'password', 'id': 'ip_2', 'class': 'fonts_fix'}))


