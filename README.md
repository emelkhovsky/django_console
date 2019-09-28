### django_console
It was created for working with linux-console.Web-site uses ***django***. 
It includes these subpages:
* registration
* authorization
* linux-console

It has block using library ***paramiko*** for connecting to server. It shows commands, answers and error messages.
Also it uses ***Mysql*** database.
There are some examples:

This is login page. It compare login and password with logins and password in Mysql database. By the way, it uses ***django.contrib.auth.models*** and supports session.
![Image alt](https://github.com/emelkhovsky/django_console/blob/master/examples/2.jpg)
There is a registration page. It sends your datas to Mysql-server.It uses django models for these goals.
![Image alt](https://github.com/emelkhovsky/django_console/blob/master/examples/3.jpg)
After authorization you need to complete user, password, ip fields from your server.
![Image alt](https://github.com/emelkhovsky/django_console/blob/master/examples/4.jpg)
Then if all is okay you get the console.
![Image alt](https://github.com/emelkhovsky/django_console/blob/master/examples/5.jpg)
You can write commands and get answers in console.
![Image alt](https://github.com/emelkhovsky/django_console/blob/master/examples/6.jpg)
