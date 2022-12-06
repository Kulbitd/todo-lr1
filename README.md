Запуск без применения Докера

uvicorn main::app --reload

Создание Докер контейнера

sudo docker build -t 2020-4-11-lr1

Создание Докер контйенера разработчика

sudo docker run --rm -v ${pwd}/app:/code/app 80:80 2020-4-11-lr1

Запуск скрипта по созданию туду

sudo docker run --rm --network=host 2020-4-11-lr1

Создание Докера через прокси

sudo docker --build-arg PROXY=http://login:pass@192.168.232.1:3128 -t 2020-4-11-lr1
