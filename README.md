# Pom Pom Project

204113 Computer Science Chiangmai University

## Introduction

Final project for [204113] Principles of Computing.

Our project is **Free Popcorn**.

**Free Popcorn** is website for reviewer and someone who love in movie,furthermore reviewer can get income from review.

## Run

Run Django
```
$ python manage.py runserver
```
Run Elasticsearch
```
cd elasticsearch-1.7.6>
./bin/elasticsearch
```
Rebuild index for search
```
$ python manage.py rebuild_index
```

## Built With
[Anaconda](https://www.continuum.io/) - The leading open data science platform powered by Python.
```
https://www.continuum.io/downloads
```
[Django](https://www.djangoproject.com/) - The web framework used.
```
$ pip install django
```
[Widget Tweak](https://github.com/kmike/django-widget-tweaks) - The form field rendering in templates for Django.
```
$ pip install django-widget-tweaks
```
[Mathfilters](https://github.com/dbrgn/django-mathfilters) - The pip-installable Python 2/3 module that provides different simple math filters for Django.
```
$ pip install django-mathfilters
```
[Haystack](http://haystacksearch.org/) - The provider modular search for Django.
```
$ pip install django-haystack
```
[Elasticsearch](https://www.elastic.co) - A distributed, RESTful search and analytics engine capable of solving a growing number of use cases.

Before install Elasticsearh, you must install JAVA and set JAVA path first.

Elasticsearch 1.7.6 is support to Django.
```
https://www.elastic.co/downloads/past-releases/elasticsearch-1-7-6
```
The provider common ground for all Elasticsearch-related code in Python
```
$ pip install elasticsearch
```
[Hitcount](https://github.com/thornomad/django-hitcount) - The basic app that allows you to track the number of hits/views for a particular object.
```
$ pip install django-hitcount
```
[CKEditor](https://github.com/django-ckeditor/django-ckeditor) - WYSIWYG
```
$ pip install django-ckeditor
```
## Authors
* **Pisol Ruenin** - *Project manager / Back-end developer*
* **Krissada Bunthong** - *Front-end developer*
* **Chutigarn Singfigaew** - *Front-end developer*
* **Sawarin Tipwiang** - *Back-end developer*
* **Apisit Kuntawat** - *Front-end developer*
* **Arormon Junsrisom** - *Back-end develper*