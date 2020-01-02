# Blackjack API
Flask API made to simulate a Blackjack game without real money betting.

## Run locally
export FLASK_APP=api/app.py 
export FLASK_ENV=development
flask run

## Run in docker compose
docker-compose up

## Create a new migration
python migrate.py make:migration <migration_name> --table <table_name> --create

## Apply the migration locally
python migrate.py migrate
python migrate.py migrate:status
