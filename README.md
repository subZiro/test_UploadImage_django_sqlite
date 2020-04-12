# test_UploadImage_django_sqlite
Imagehost django+sqlite



## Installation with github
clone:
```sh
git clone https://github.com/subZiro/test_UploadImage_django_sqlite.git
```

virtual env:
```sh
python3 -m venv venv 
source venv/bin/activate
```

install requirements:
```sh
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

directery manage.py
```sh
cd project
```

 run
```sh
python manage.py runserver 5000
```



### run with docker 


clone:
```sh
git clone https://github.com/subZiro/test_UploadImage_django_sqlite.git
```

create image:
```sh
cd project
docker build -t test_django .
```

run image:
```sh
docker run -d -p 5000:5000 --name test_django_d test
```


### open 127.0.0.1:5000 in browser






## Index page
![index page](https://github.com/subZiro/test_UploadImage_django_sqlite/blob/master/index.jpg)


## Upload page
![upload](https://github.com/subZiro/test_UploadImage_django_sqlite/blob/master/upload.jpg)


## View page
![view](https://github.com/subZiro/test_UploadImage_django_sqlite/blob/master/view-edit.jpg)
