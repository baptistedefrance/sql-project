#!/bin/sh
database1="tpb2.db"
database2="migration.db"

echo "Welcome on SQL_MIGRATION_B2 Menu !"

echo "Please, select an option : "

echo "1/ Create schema"

echo "2/ Transfert DATABASE"

echo "3/ List some information"

echo "4/ Delete all"

echo "5/ See all database"

echo "6/ Make every options"

read input

echo "You choose $input option"

if [ $input == 1 ]
then
 echo "Create schema starting..."
 sqlite3 $database2 < schema.sql
 echo "Create schema complete"
fi

if [ $input == 2 ]
then
 echo "Database transfert starting..."
 sqlite3 $database2 < migration.sql
 echo "Database transfert complete"
fi

if [ $input == 3 ]
then
 echo "List some information starting..."
 sqlite3 $database2 < queries.sql
 echo "List some information complete"
fi

if [ $input == 4 ]
then
 echo "Delete all starting..."
 sqlite3 $database2 < drop.sql
 echo "Make every option complete"
fi

if [ $input == 5 ]
then
 echo "See all database starting..."
 sqlite3 $database2 
 echo "See all database complete"
fi

if [ $input == 6 ]
then
 echo "Make every option starting..."
 sqlite3 $database2 < schema.sql
 sqlite3 $database2 < migration.sql
 sqlite3 $database2 < queries.sql
 echo "Make every option complete"
fi

