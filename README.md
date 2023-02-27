# Python-Login-app
An app which checks database for login operations. You can register or login in this account and store your datas in a MySql server.

If you want to use that app, firstly you have to create a python file named "emailim.py" in the same folder. Then you have to create 2 variables. First one is my_email and
the other one is password. You should enter your gmail account in string form. Also you have to create a mysql database and create a table named "users". Then add these
properties: id (int, primary key, unique key, not null, auto increament) username (varchar(45) not null) password (varchar(45) not null) and email (varchar(255) not null)

After you created the database get into the code and change the places where we connect to the database with the correct ones. Now you are ready.
