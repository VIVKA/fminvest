#!/bin/bash
clear
echo "Databases"

sudo docker run --name factota-postgres -d postgres -p 5432:5432 postgres:10-alpine

