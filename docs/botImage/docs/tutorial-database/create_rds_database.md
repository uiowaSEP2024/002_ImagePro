---
sidebar_position: 1
---

# Create RDS Database

1. Assuming you have access to an AWS console to work on, login to your console and navigate to RDS > Database.
2. When creating an RDS, this is assumed on the fact a VPC is created by you and you have access to it in the console.
3. In RDS > Database, click on Create Database on the top right corner of the page.
4. Once you are in the Create Database page, In `Choose a database creation method`, select Standard Create.
5. In the `engine options` section, Select PostgreSQL as `engine type`, and `engine version` PostgreSQL 14.6-R1.
6. In the `Templates` section, assuming you are working on Development of the application, choose Dev/Test. When moving to production later, choose production in this step.
7. In the `availability and durabililty` section, select `Multi-AZ DB Cluster`.
8. In the `Settings` section, type in your DB identifer(Name of Your DB), your master username and your master password.
9. In `Instance Configuration`, select Standard classes.
10. Stick to the already selected options in the `Storage` option.
 
 ### Looks like you are done! Click on the create Database button and you will have a running instance of your Database in AWS!
