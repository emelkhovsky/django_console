from django.shortcuts import render, redirect
from .forms import reg_form,log_form, ip_form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from riddles.models import Ipdata_model
import paramiko


def log(request, logform):
    login = logform.cleaned_data['log_login']
    password = logform.cleaned_data['log_password']
    user = authenticate(username=login, password=password)
    if user is not None:
        request.session['username'] = login
        messages.error(request, 'Вы успешно вошли!')
    else:
        messages.error(request, 'Неправильный логин или пароль!')

def ip_(request, ipform):
    if 'username' not in request.session:
        messages.error(request, 'Сначала авторизируйтесь!')
    else:
        name = ipform.cleaned_data['ip_user']
        password = ipform.cleaned_data['ip_password']
        ip = ipform.cleaned_data['ip_ip']
        return render(request, 'riddles/console.html')

def log_out(request):
    request.session.flush()
    return None

def name_function(request):
    name = 'Anonymus'
    if 'username' in request.session:
        name = request.session['username']
    return name

def name_flag_function(request):
    name_flag = None
    if 'username' in request.session:
        name_flag = 1
    return name_flag

def main(request):
    name = name_function(request)
    name_flag = name_flag_function(request)

    logform = log_form()
    ipform = ip_form()

    if request.method == 'POST':
        logform = log_form(request.POST)
        ipform = ip_form(request.POST)
        if logform.is_valid():
            log(request, logform)
            name = name_function(request)
            name_flag = name_flag_function(request)
        elif ipform.is_valid():
            ip_(request, ipform)
        else:
            name_flag = log_out(request)
            name = name_function(request)

    context = {
        'logform': logform,
        'ipform': ipform,
        'name': name,
        'title_name': main,
        'name_flag': name_flag,
    }
    return render(request, 'riddles/log.html', context)

def reg_processing(request, regform):
    login = regform.cleaned_data['login']
    password = regform.cleaned_data['password']
    email = regform.cleaned_data['email']
    user = User.objects.create_user(username = login, email = email, password = password)
    user.save()
    ipdata = Ipdata_model(ip_username = login)
    ipdata.save()
    messages.error(request, 'Вы успешно зарегистрировались!')

def reg(request):
    name = name_function(request)
    name_flag = name_flag_function(request)

    ipform = ip_form()
    regform = reg_form()

    if request.method == 'POST':
        regform = reg_form(request.POST)
        if regform.is_valid():
            reg_processing(request, regform)
        else:
            name_flag = log_out(request)
            name = name_function(request)
    context = {
        'regform': regform,
        'title_name':'registration',
        'ipform':ipform,
        'name':name,
        'name_flag':name_flag,
    }
    return render(request, 'riddles/reg.html', context)

def commands_processing(ip, name_from_ip, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = ip, username = name_from_ip, password = password)
    stdin, stdout, stderr = ssh.exec_command(command)
    stdout = stdout.read().decode('utf-8')
    stderr = stderr.read().decode('utf-8')
    return stdout, stderr


all_console = []
def console(request):
    name = name_function(request)
    name_flag = name_flag_function(request)
    ipform = ip_form()

    if request.method == 'POST':
        if request.POST.get('logout'):
            name_flag = log_out(request)
            name = name_function(request)
        if request.POST.get('start'):
            ipform = ip_form(request.POST)
            if ipform.is_valid():
                ipdata = Ipdata_model.objects.get(ip_username = request.session['username'])
                ipdata.ip_ip = ipform.cleaned_data['ip_ip']
                ipdata.ip_user = ipform.cleaned_data['ip_user']
                ipdata.ip_password = ipform.cleaned_data['ip_password']
                ipdata.save()
        if request.POST.get('command_input'):
            command = request.POST['command_input']
            ipdata = Ipdata_model.objects.get(ip_username = request.session['username'])
            print(ipdata.ip_ip, ipdata.ip_user, ipdata.ip_password)
            if ipdata.ip_ip is not None:
                ip = ipdata.ip_ip
                name_from_ip = ipdata.ip_user
                password = ipdata.ip_password
                stdout, stderr = commands_processing(ip, name_from_ip, password, command)
                all_console.append(command)
                all_console.append(stdout)
                all_console.append(stderr)
            else:
                messages.error(request, 'Сначала подключитесь!')

    if 'username' not in request.session:
        messages.error(request, 'Сначала авторизируйтесь!')
        logform = log_form()
        context = {
            'title_name': 'main',
            'ipform':ipform,
            'loform':logform,
            'name': name,
            'name_flag': name_flag,}
        return redirect('/', context)

    print(all_console)
    context = {
        'title_name': 'console',
        'ipform': ipform,
        'name': name,
        'name_flag': name_flag,
        'all_console': all_console,
    }
    return render(request, 'riddles/console.html', context)


