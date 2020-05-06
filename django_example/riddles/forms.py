from django import forms

class reg_form(forms.Form):
    login = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'login', 'id': 'reg_1', 'class': 'fonts_fix'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'password', 'id': 'reg_2', 'class': 'fonts_fix'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'email', 'id': 'reg_3', 'class': 'fonts_fix'}))

class log_form(forms.Form):
    log_login = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'login', 'id': 'log_1', 'class': 'fonts_fix'}))
    log_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'password', 'id': 'log_2', 'class': 'fonts_fix'}))

class input_form(forms.Form):
    input_line = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '', 'id': 'command_input', 'class': 'under_question'}))


'''class input_form(forms.ModelForm):
    class Meta:
        model = InputCommandsModel
        fields = ['input_line']
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'post-commands',
                'required': True,
                'placeholder': ''
            }),
        }'''