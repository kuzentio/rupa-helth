Rupa Health
================

This is home assignment for Rupa Health.

How it works
-----------------------
This application is designed for sending emails by using two email providers: Mailgun and Postmark.
It tries to send email using default provider, and once it fails, it tries to send email using second provider.

Configuration
-----------------------
The list of available Email providers is defined in `settings.py` file:
```python
EMAIL_PROVIDERS = [
    {
        'class': 'emails.providers.PostmarkEmailProvider',
    },
    {
        'class': 'emails.providers.MailgunEmailProvider',
    },
]
```
The first email provider in the list is default one.

The application could be configured in multiple persistence modes.
First is to save `all` email and second is to save only email which `failed` to send.
I can be configured accordingly as `all` or `failed`:
```python
PERSISTENCE_MODE = all
``` 

Usage
-----------------------
#### 1. Populate environment variables
This repository contains `.env.example` file. 
Please rename it to `.env` 
```bash
mv .env.example .env
```
and populate with your credentials.

### 2. Run application
This application could be ran in two ways:
- by using docker-compose
- by using python virtual environment

#### 2.1. Run application by using docker-compose
In order to run application by using docker-compose, please run following command:
```bash
docker-compose up
```
#### 2.2. Run application by using python virtual environment
In order to run application by using python virtual environment, please run following commands:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Send email
Neither Postmark nor Mailgun allows to register with public email providers such as gmail.com, yahoo.com, etc.
So I used temporary generated emails provider https://temp-mail.org/ to register in those services.
We need to be aware that sender should be registered with the same email provider.


### Languages and Frameworks used
I used Python and Django Rest Framework to implement this application.
Advantages of using Django Rest Framework are:
- it is easy to implement REST API
- it is easy to implement persistence layer
- it is easy to implement configuration layer

### Implementation trade-offs
I made saving email to database optional, so it could be configured to save all emails or only failed ones.
It wasn't reflected in Technical Assessment doc, but I decided to add saving email into database as it could be useful for debugging purposes.


### The duration dedicated to completing this task 
I spent around 8 hours to complete this task.

### What I would have done differently if you had had more time
I would have to add Celery to send emails asynchronously which allows to scale application.

I would add more latency, failure metrics for this service.
I would add into EmailService retry mechanism. I would add additional method for returning failed email.

