## Setup Instruction
```
poetry install
```

## Run Test
```
poetry run pytest
```

## Run Application
Set up postgresql then save the database information in .env file as the followings:
```
DB_USER={YOUR_DB_USER}
DB_PASS={YOUR_DB_PASSWORD}
DB_PORT={YOUR_DB_PORT}
DB_HOST={YOUR_DB_HOST}
```

Then create database "vending_machine"
```
CREATE DATABASE "vending_machine";
```

Then you are good to go!!!
Here are the apis
```
-list all stocks
-add vending
-edit vending
-delete vending
-add stock
-edit stock
-delete stock
```
