# Project Flask And Django-admin

Welcome to the admin + flask repository! This project aims to automate network tasks using Flask, Flask-Migrate, Netmiko, PyEZ, ipaddress, and other libraries, combined with authentication and user management through the Django Admin interface and database.

## Previews

## Main Django Page
![alt text](https://github.com/Richardbarbosasilva/flask-django-admin/blob/main/Previews/preview3.gif)

![alt text](https://github.com/Richardbarbosasilva/flask-django-admin/blob/main/Previews/django-admin1.png)

## Main Flask Page
![alt text](https://github.com/Richardbarbosasilva/flask-django-admin/blob/main/Previews/flask1.png)

## Dashboards and Menus
![alt text](https://github.com/Richardbarbosasilva/flask-django-admin/blob/main/Previews/preview2.gif)

## User, group and permission management
![alt text](https://github.com/Richardbarbosasilva/flask-django-admin/blob/main/Previews/preview1.gif)

## Flask HTTP error 403
![alt text](https://github.com/Richardbarbosasilva/flask-django-admin/blob/main/Previews/403.png)

#######################################################################################################################

## 📌 Features

- Network device integration with **NETCONF** e **RESTCONF**
- Vlan management and network prefixs
- Django-admin integration and authentication
- IP Validation
- Supports both Datacom and Juniper devices

## 🚀 How to run the project (debian based distros)

### 1️⃣ Clone the repository
```bash
https://github.com/Richardbarbosasilva/flask-django-admin.git
```

### Create virtual enviroment
```bash
active virtual enviroment inside the project root:
source venv/bin/activate

```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run application Flask (needs gunicorn and nginx successfully set)
```bash
Flask application run:
gunicorn -w 4 run:app --bind 0.0.0.0:<your-port>
```

### Run application Django-Admin (needs gunicorn and nginx successfully set)
```bash
Flask application run:
gunicorn -w 4 run:app --bind 0.0.0.0:<your-port>
```
### Run application Django (needs gunicorn and nginx successfully set)
```bash
Set virtual enviroment in another server instance just like the steps before
Django application run:
gunicorn -w 4 elevate.wsgi:application --bind 0.0.0.0:<your-port>
```

Access **http://<you-server-ip-address>** on browser.


## 📝 Licença
This project is under MIT Licence. Feel free to modify as you will! 🎉

