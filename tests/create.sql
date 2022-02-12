CREATE TABLE student(id int(10) auto_increment PRIMARY KEY, name varchar(15), gender char(1), age int(3));
Create table articles(id int(10) auto_increment PRIMARY KEY, author_id int(10),title varchar(30), content text);
Create table authors(id int(10) auto_increment PRIMARY KEY, name varchar(30));