---
sidebar_position: 1
---

# Create RDS Database

1. Assuming you have access to an AWS console to work on, login to your console and navigate to RDS > Database.
2. When creating an RDS, this is assumed on the fact a VPC is created by you and you have access to it in the console.
3. In RDS > Database, click on Create Database on the top right corner of the page.
4. Once you are in the Create Database page, In `Choose a database creation method`, select Standard Create.
![Choose a database creation method](/img/Choose-a-database-creation-method.png)
5. In the `engine options` section, Select PostgreSQL as `engine type`, and `engine version` PostgreSQL 14.6-R1.
![Engine Options](/img/Engine-Options.png)
6. In the `Templates` section, assuming you are working on Development of the application, choose Dev/Test. When moving to production later, choose production in this step.
7. In the `availability and durabililty` section, select `Multi-AZ DB Cluster`.
![Templates](/img/Templates.png)
8. In the `Settings` section, type in your DB identifer(Name of Your DB), your master username and your master password.
9. In `Instance Configuration`, select Standard classes.
10. Stick to the already selected options in the `Storage` option.
 
Looks like you are done! Click on the create Database button and you will have a running instance of your Database in AWS!

 ## Connecting to the instance of your RDS in your DB Editor

 1. Assuming you are performing all SQL queries and viewing all tables in pgAdmin 4, open the software and login to your pgAdmin server.
 2. In RDS > Databases, select your newly created Database instance and navigate in to view DB endpoint
    ![DB Endpoint](/img/DB-Endpoint.png)
3. Copy your endpoint and keep it ready for loading in pgAdmin.
4. In pgAdmin, right click on Servers and select Create > Server.
5. Add a name for your server and click on server, a pop up menu will show.
6. In the `General` tab, type in your server name and in the `Connection` tab, type in your DB endpoint in the `Host name/address` field. Your port number will be **5432** (Standard port for all PG databases).
7. In the `Connection` tab, type in your master username in the `Username` field and your master password in the `Password` field.
8. Click on save and you will have your server connected to your DB instance.
9. You can now view all your tables and perform SQL queries in your DB instance.