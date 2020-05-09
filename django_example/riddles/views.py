from django.shortcuts import render
from .forms import reg_form,log_form, input_form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
import paramiko
from django.http import HttpResponse
import json
import time
import re
from riddles.models import Progress_model
from urllib.parse import unquote

all_console = {}
connection_dict = {}
ban_commands = {'cd ~', 'cd /', 'cd /root', 'cd /home', 'su -', 'useradd', 'userdel', 'usermod', 'passwd', 'sudo', 'ping', 'rm -rf /*', 'apt-get', 'wget', 'apt', 'python', 'kill', 'pkill', 'ps -aux'}#список запрещенных команд


def connection(login):
    ip = '185.204.0.41'
    password = 'yL5t690i76R1'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, username=login, password=password)
    channel = ssh.invoke_shell()
    connection_dict[login] = channel
    all_console[login] = []


def log_processing(request, logform):
    login = logform.cleaned_data['log_login']
    password = logform.cleaned_data['log_password']
    user = authenticate(username=login, password=password)
    if user is not None:
        request.session['username'] = login
        connection(login)
        messages.error(request, 'Вы успешно вошли!')
    else:
        messages.error(request, 'Неправильный логин или пароль!')


def log_out(request):#выход из учетной записи
    name = name_function(request)
    try:
        connection_dict.pop(name)
    except:
        print('ok1')
    try:
        all_console.pop(name)
    except:
        print('ok1')
    request.session.flush()
    return None

def name_function(request):#смотрим имя человека
    name = 'Anonymus'
    if 'username' in request.session:
        name = request.session['username']
    return name

def name_flag_function(request):#определяем авторизирован человек или нет, возвращаем флажок
    name_flag = None
    if 'username' in request.session:
        name_flag = 1
    return name_flag

def login(request):
    logform = log_form()

    if request.method == 'POST':
        logform = log_form(request.POST)
        if logform.is_valid():
            log_processing(request, logform)

    context = {
        'logform': logform,
        'name': None,
        'title_name': 'login',
        'name_flag': None,
    }
    return render(request, 'riddles/log.html', context)

def main(request):
    name = name_function(request)
    name_flag = name_flag_function(request)

    logform = log_form()

    if request.method == 'POST':
        logform = log_form(request.POST)
        if logform.is_valid():
            log_processing(request, logform)
            name = name_function(request)
            name_flag = name_flag_function(request)
        else:
            name_flag = log_out(request)
            name = name_function(request)
    context = {
        'logform': logform,
        'name': name,
        'title_name': 'main',
        'name_flag': name_flag,
    }
    return render(request, 'riddles/main.html', context)


def progress(request):#отображение страницы прогресса
    if not name_flag_function(request):
        return HttpResponseRedirect('/')
    name = name_function(request)
    name_flag = name_flag_function(request)

    progressmodel_dict = Progress_model.objects.filter(username=name).values()[0]
    score_value = progressmodel_dict['score']
    all_answers_value = progressmodel_dict['all_answers']
    good_answers_value = progressmodel_dict['good_answers']
    kol_lessons_value = progressmodel_dict['kol_lessons']
    course_percent = int(kol_lessons_value / 6 * 100)
    if all_answers_value != 0:
        percent = int(good_answers_value / all_answers_value * 100)
    else:
        percent = 0
    progressmodel = Progress_model.objects.all().order_by('-score')
    progressmodel = progressmodel[:3].values()
    first_raiting_score = progressmodel[0]['score']
    second_raiting_score = progressmodel[1]['score']
    third_raiting_score = progressmodel[2]['score']
    first_raiting_username = progressmodel[0]['username']
    second_raiting_username = progressmodel[1]['username']
    third_raiting_username = progressmodel[2]['username']
    context = {
        'name': name,
        'title_name': 'progress',
        'name_flag': name_flag,
        'score_value': score_value,
        'percent': percent,
        'first_raiting_score': first_raiting_score,
        'second_raiting_score': second_raiting_score,
        'third_raiting_score': third_raiting_score,
        'first_raiting_username': first_raiting_username,
        'second_raiting_username': second_raiting_username,
        'third_raiting_username': third_raiting_username,
        'kol_lessons_value': kol_lessons_value,
        'course_percent': course_percent,
    }
    return render(request, 'riddles/progress.html', context)

def reg_processing(request, regform):
    login = regform.cleaned_data['login']
    password = regform.cleaned_data['password']
    email = regform.cleaned_data['email']
    try:
        user = User.objects.create_user(username=login, email=email, password=password)
        user.save()
        progressmodel = Progress_model(username=login, score=0, kol_lessons=0, all_answers=0, good_answers=0)
        progressmodel.save()
        messages.error(request, 'Вы успешно зарегистрировались!')
    except:
        messages.error(request, 'Данный пользователь уже зарегистрирован, попробуйте еще раз(или проверьте корректность email)')

    ip = '185.204.0.41'
    name_from_ip = 'root'
    password = 'yL5t690i76R1'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, username=name_from_ip, password=password)
    channel = ssh.invoke_shell()
    connection_dict['root'] = channel
    print(create_output('useradd -m ' + login, 'root'))
    print(create_output('passwd ' + login, 'root'))
    print(create_output(password, 'root'))
    print(create_output(password, 'root'))
    ssh.close()


def reg(request):
    name = name_function(request)
    name_flag = name_flag_function(request)
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
        'name':name,
        'name_flag':name_flag,
    }
    return render(request, 'riddles/reg.html', context)



#---------------------------------------------уроки----------------------------------------

def ending_lesson_processing(name):#добавление баллов за прохождение урока
    progressmodel_dict = Progress_model.objects.filter(username=name).values()[0]
    score_value = progressmodel_dict['score']
    kol_lessons_value = progressmodel_dict['kol_lessons']
    if kol_lessons_value != 5:
        kol_lessons_value += 1
    score_value += 100
    Progress_model.objects.filter(username=name).update(score=score_value, kol_lessons=kol_lessons_value)

def lesson1(request):
    if not name_flag_function(request):
        return HttpResponseRedirect('/')
    name = name_function(request)
    name_flag = name_flag_function(request)
    inputform = input_form()
    if request.method == 'POST':
        if request.POST.get("hh"):
            ending_lesson_processing(name)
            return HttpResponseRedirect('/lesson2/')
    context = {
        'name': name,
        'title_name': 'lesson1',
        'name_flag': name_flag,
        'all_console': all_console[name],
        'inputform': inputform,
    }
    return render(request, 'riddles/lesson1.html', context)

def lesson2(request):
    if not name_flag_function(request):
        return HttpResponseRedirect('/')
    name = name_function(request)
    name_flag = name_flag_function(request)
    inputform = input_form()
    if request.method == 'POST':
        if request.POST.get("hh"):
            ending_lesson_processing(name)
            return HttpResponseRedirect('/lesson3/')
    context = {
        'name': name,
        'title_name': 'lesson2',
        'name_flag': name_flag,
        'all_console': all_console[name],
        'inputform': inputform,
    }
    return render(request, 'riddles/lesson2.html', context)

def lesson3(request):
    if not name_flag_function(request):
        return HttpResponseRedirect('/')
    name = name_function(request)
    name_flag = name_flag_function(request)
    inputform = input_form()
    if request.method == 'POST':
        if request.POST.get("hh"):
            ending_lesson_processing(name)
            return HttpResponseRedirect('/lesson4/')
    context = {
        'name': name,
        'title_name': 'lesson3',
        'name_flag': name_flag,
        'all_console': all_console[name],
        'inputform': inputform,
    }
    return render(request, 'riddles/lesson3.html', context)

def lesson4(request):
    if not name_flag_function(request):
        return HttpResponseRedirect('/')
    name = name_function(request)
    name_flag = name_flag_function(request)
    inputform = input_form()
    if request.method == 'POST':
        if request.POST.get("hh"):
            ending_lesson_processing(name)
            return HttpResponseRedirect('/lesson5/')
    context = {
        'name': name,
        'title_name': 'lesson4',
        'name_flag': name_flag,
        'all_console': all_console[name],
        'inputform': inputform,
    }
    return render(request, 'riddles/lesson4.html', context)

def lesson5(request):
    if not name_flag_function(request):
        return HttpResponseRedirect('/')
    name = name_function(request)
    name_flag = name_flag_function(request)
    inputform = input_form()
    if request.method == 'POST':
        if request.POST.get("hh"):
            ending_lesson_processing(name)
            return HttpResponseRedirect('/lesson6/')
    context = {
        'name': name,
        'title_name': 'lesson5',
        'name_flag': name_flag,
        'all_console': all_console[name],
        'inputform': inputform,
    }
    return render(request, 'riddles/lesson5.html', context)

def lesson6(request):
    if not name_flag_function(request):
        return HttpResponseRedirect('/')
    name = name_function(request)
    name_flag = name_flag_function(request)
    inputform = input_form()
    if request.method == 'POST':
        if request.POST.get("hh"):
            progressmodel_dict = Progress_model.objects.filter(username=name).values()[0]
            score_value = progressmodel_dict['score']
            score_value += 600#100+500
            kol_lessons_value = progressmodel_dict['kol_lessons']
            if kol_lessons_value != 5:
                kol_lessons_value += 1
            Progress_model.objects.filter(username=name).update(score=score_value, kol_lessons=kol_lessons_value)
            return HttpResponseRedirect('/progress/')
    context = {
        'name': name,
        'title_name': 'lesson6',
        'name_flag': name_flag,
        'all_console': all_console[name],
        'inputform': inputform,
    }
    return render(request, 'riddles/lesson6.html', context)

#--------------------------------работа с ajax запросом------------------------------------------

def create_post(request):
    name = name_function(request)
    if request.method == 'POST' and request.is_ajax:
        if request.POST.get('command_input'):
            console(request)
            return HttpResponse(json.dumps(all_console[name]), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")

#--------------------------------console------------------------------------------

def create_output(command, name):
    channel = connection_dict.get(name)
    channel.send(command + '\n')
    time.sleep(1)
    output = channel.recv(2024).decode('utf-8')
    ind = output.find(command)
    ind = output.find(command, ind + 1)
    ind_start_output = ind + len(command) + 1
    ind_end_output = output.find('root@emelkhovsky4', ind_start_output)
    output = output[ind_start_output: ind_end_output]
    return str(output)


def console(request):
    command = request.POST['command_input']
    command = command[96:]
    command = unquote(command)
    flag = 0
    output = ''
    name = name_function(request)
    if command not in ban_commands:
        command_list = command.split(' ')
        for i in command_list:
            if i in ban_commands:
                output = 'Command is not allowed, sorry :('
                flag = 1
        if flag == 0:
            if command == 'clear':
                all_console[name].clear()
            elif command == 'cd ..':
                if create_output('pwd', name).count('/') > 2:
                    output = create_output(command, name)
                else:
                    output = 'Command is not allowed, sorry :('
            elif command == 'cd ../..':
                if create_output('pwd', name).count('/') > 3:
                    output = create_output(command, name)
                else:
                    output = 'Command is not allowed, sorry :('
            elif 'history' in command:
                print('hist')
            else:
                output = create_output(command, name)

        if 'come to Ubuntu 16.04.6 LTS' in output:
            output = create_output(command, name)

    else:
        output = 'Command is not allowed, sorry :('

    progress_processing(request, output)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    output = ansi_escape.sub('', output)
    all_console[name].append(command)
    all_console[name].append(output)


def progress_processing(request, output):#обработка правильных и неправильных ответов
    name = name_function(request)
    progressmodel_dict = Progress_model.objects.filter(username=name).values()[0]
    score_value = progressmodel_dict['score']
    all_answers_value = progressmodel_dict['all_answers']
    good_answers_value = progressmodel_dict['good_answers']
    all_answers_value += 1
    if 'not found' in output:
        score_value -= 10
    else:
        score_value += 10
        good_answers_value += 1
    Progress_model.objects.filter(username=name).update(score=score_value, good_answers=good_answers_value, all_answers = all_answers_value)






