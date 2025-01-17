#!/usr/bin/env bash


echo "Ensure database table has been setup..."
# run setup script for setup to create table on dynamodb
python app/database/setup.py

echo "Start FastAPI..."
# launch fastapi
fastapi run app/main.py --port 80
