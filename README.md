Clone repository to local directory with:
```
git clone https://github.com/murekswork/zakupki_solution
cd zakupki_crawler
```
Create docker containers with:
```
docker compose up --build
```
To run unittest write in separate terminal:
```
docker compose exec worker python -m unittest discover tests
```
To run application write in separate terminal:
```
docker compose exec worker python main.py
```
