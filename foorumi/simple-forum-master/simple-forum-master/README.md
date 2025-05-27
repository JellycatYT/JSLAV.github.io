# Simple-forum
Simple forum, that allows you to post your own discussions and coments.

# Description

Current web application represent a simple forum website? where you can post different discussions, and add coments to them.
Both discussions and comments data are stored in local mysql database.
Data validation also implemented(by using Hibernate Validator).

Discussion entity are consists of: 
 - Discussion id;
 - Username;
 - Topic of dicsussion;
 - Discussion text.
 
 Comment entity:
 - comment id;
 - discussion id;
 - username;
 - comment text;
 
 # Prerequisites
 To run this project you need to install next software:
 - Java 8 - development environment;
 - Maven - dependency manager;
 - Tomcat - web server;
 - MySQL - database;
 
# Technologies used
- Maven
- Spring MVC 5.2.1
- Spring Boot
- Thymeleaf 3.0.11
- Hibernate Validator 6.1.6
- Mysql Connector 8.0.23
- JPA
