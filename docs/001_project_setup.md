# Project Setup Instructions

## Prerequisites

- A Debian/Ubuntu-based Linux system
- `sudo` access
- Git

---

## Step 1: Install System Dependency Packages

```sh
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev \
xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

---

## Step 2: Install pyenv

```sh
curl https://pyenv.run | bash
```

Add the following to your `~/.bashrc`:

```sh
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Reload the shell:

```sh
source ~/.bashrc
```

---

## Step 3: Install Python 3.12.3

```sh
pyenv install 3.12.3
pyenv local 3.12.3
```

> You can also create a virtual environment here if you are not using the system Python (e.g. in a deployment setup).
```sh
python -m venv .venv
```

---

## Step 4: Clone the Repository

```sh
git clone https://github.com/tsvtln/GameAndMediaTracker.git
cd GameAndMediaTracker
```

---

## Step 5: Configure Environment Variables

Copy the template and fill in your values:

```sh
cp .env_example .env
```

Edit `.env` with the required values:

| Variable               | Description                                    |
|------------------------|------------------------------------------------|
| `SECRET_KEY`           | Django secret key                              |
| `DEBUG`                | `True` for development, `False` for production |
| `ALLOWED_HOSTS`        | Comma-separated list of allowed hosts          |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins for CSRF       |
| `DATABASE_NAME`        | PostgreSQL database name                       |
| `DATABASE_USER`        | PostgreSQL user                                |
| `DATABASE_PASSWORD`    | PostgreSQL password                            |
| `DATABASE_HOST`        | Database host (e.g. `localhost`)               |
| `DATABASE_PORT`        | Database port (default `5432`)                 |
| `CELERY_BROKER_URL`    | Redis URL (e.g. `redis://localhost:6379/0`)    |

_**NOTE:** If you setup a REDIS password, the `CELERY_BROKER_URL` should include it like: `redis://:<password>@localhost:6379/0`_

---

## Step 6: Install PostgreSQL

```sh
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

### Create the Database and User

```sh
sudo -u postgres psql
```

Inside the PostgreSQL shell, run:

```sql
CREATE DATABASE <your_database_name>;

CREATE USER <your_user> WITH PASSWORD '<your_password>';

ALTER ROLE <your_user> SET client_encoding TO 'utf8';
ALTER ROLE <your_user> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <your_user> SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE <your_database_name> TO <your_user>;
```

### Allow Password Authentication

Open the PostgreSQL host-based authentication config:

```sh
sudo vi /etc/postgresql/*/main/pg_hba.conf
```

Find this line:

```
local   all             all                                     peer
```

Change it to:

```
local   all             all                                     md5
```

Restart the service:

```sh
sudo systemctl restart postgresql
```

You can verify the connection manually afterwards:

```sh
psql -U <your_user> -d <your_database_name> -h localhost -W
```

---

## Step 7: Install Python Dependencies

Navigate to the cloned repository and run:

```sh
pip install -r ./requirements.txt
```

---

## Step 8: Populate the Database and Create an Admin Account

Run all migrations, populate the required user groups and forum boards, then create a superuser:

```sh
python manage.py migrate
python manage.py create_user_groups
python manage.py populate_forum
python manage.py createsuperuser
```

Groups created by `create_user_groups`:
- **Regular Users** - default group assigned to every new registrant
- **Moderators** - can delete any content, manage events/forums
- **Verified Users** - can upload BIOS files

---

## Step 9: Fix Media Folder Permissions

```sh
sudo chmod -R 2775 ./media
```
  
  
_**Note**: If you are hosting the app (e.g. with nginx + gunicorn), you may also need to change the owner and set up groups appropriately:_

```sh
sudo chown -R <your_user>:www-data ./media
```

---

## Step 10: Install and Start Redis

```sh
sudo apt install redis-server -y
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

Or using Docker:

```sh
docker run -d -p 6379:6379 redis
```

---

## Step 11: Start the Celery Worker

In a separate terminal (with the correct Python environment active):

```sh
celery -A CheckPoint worker --loglevel=info
```

To also run the periodic beat scheduler:

```sh
celery -A CheckPoint beat --loglevel=info
```

---

## Step 12: Run the Development Server

```sh
python manage.py runserver
```

By default, the server runs at http://127.0.0.1:8000/.

---

## Running Tests

Tests are located in the `tests/` directory at the project root.

```sh
python manage.py test
```

---

#### Next Page: [Models](002_models.md)

---

<div style="display: flex">
  <a href="../README.md">
    <svg width="20" height="20" fill="blue" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" version="1.1" id="Capa_1" width="800px" height="800px" viewBox="0 0 495.398 495.398" xml:space="preserve">
    <g>
        <g>
            <g>
                <path d="M487.083,225.514l-75.08-75.08V63.704c0-15.682-12.708-28.391-28.413-28.391c-15.669,0-28.377,12.709-28.377,28.391     v29.941L299.31,37.74c-27.639-27.624-75.694-27.575-103.27,0.05L8.312,225.514c-11.082,11.104-11.082,29.071,0,40.158     c11.087,11.101,29.089,11.101,40.172,0l187.71-187.729c6.115-6.083,16.893-6.083,22.976-0.018l187.742,187.747     c5.567,5.551,12.825,8.312,20.081,8.312c7.271,0,14.541-2.764,20.091-8.312C498.17,254.586,498.17,236.619,487.083,225.514z"/>
                <path d="M257.561,131.836c-5.454-5.451-14.285-5.451-19.723,0L72.712,296.913c-2.607,2.606-4.085,6.164-4.085,9.877v120.401     c0,28.253,22.908,51.16,51.16,51.16h81.754v-126.61h92.299v126.61h81.755c28.251,0,51.159-22.907,51.159-51.159V306.79     c0-3.713-1.465-7.271-4.085-9.877L257.561,131.836z"/>
            </g>
        </g>
    </g>
    </svg>
  </a>
 <a style="margin-left: 10px" href="../README.md">Home</a>
</div>

---

