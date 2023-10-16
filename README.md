# My store
My project, stack:
* Python
* Django
* DRF
* PostgreSQL
* HTML 

in the future I plan to connect:

* Redis
* Celery



# Local Developing
All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
```python
python3.9 -m venv ../venv
source ../venv/bin/activate
```
2. Install packages:

```python
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
3. Run project dependencies, migrations, fill the database with the fixture data etc.:

```python
./manage.py migrate
./manage.py loaddata <path_to_fixture_files>
./manage.py runserver 
```
