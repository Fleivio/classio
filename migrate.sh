rm -rf migrations
rm app_database.sqlite
flask db init 
flask db migrate -m "new migration"
flask db upgrade