**Team 03 README**

**Team Members:** Himanshu Bainwala, Rexford Essilfie, Ryan Edwall, Anand Gopalakrishnan, and Mira Tellegen

**Client:** Professor Hans Johnson

**Project:** BotImage, an AWS RDS which accepts JSON output from a python script in a VPC, validates the schema, and catalogs progress and billing through a variable and extensible number of steps. Accompanied by a web app where clients and admin can view jobs, job progress, and billing.

**Meeting Schedule**  

Stand ups: Tuesday, Thursday, Sunday 9pm  

Sprint Retrospective: Sunday after sprint end  

Sprint Planning: Monday of sprint start  


**Project Goals**

Our client wants a cloud solution in the form of an AWS RDS for JSON logging from multiple sources.

The initial case study would be the BotImage Python cancer detection script, where in 20-steps, medical images are analyzed. The existing python program runs both in hospitals and at corporate headquarters, and outputs printf statements as each step is completed or fails. Those print statements are then parsed for progress and billing info.

The goal is to roll BotImage over such that the python script outputs a JSON with predefined schema for each of the steps. With the images sent to a VPC, the JSON would then be loaded into an AWS RDS running Postgres, and. the. schema would be validated. Schema would include the Job ID, the Client ID, the step completed, and any errors. With all data stored in the RDS, the JSON could easily be queried to keep track of billing by step, and to show a progress bar to clients.

An associated web app would allow clients to securely log in, browse their jobs, and see progress or errors for each. It would allow admin to securely log in, browse all clients, the progress of the jobs, and billing per step for each client. Admin may be able to see statistics about where errors are occurring or edit billing structure from the web app.

Outside of the BotImage case study, the cloud solution we are developing should apply generally to any type of python script that is running jobs for clients with some number of steps.

**Vocabulary and Definitions**

*Client:* We are defining a client as a company which uses the cancer detection service, or needs the python script with JSON output by step. For example, Mercy Hospital could be a client, or Noodles and Company. Clients are the groups being billed for usage.

*End-User:* We are defining an end-user as an individual person signing into the web app. End users can sometimes be admin. A user might be a tech at the hospital signing in for results from their studies they have submitted. An admin user would be someone at the BotImage company who provides the analysis tool, and signs in to see client job progress or to manage billing.

**Tech Stack**

*Framework*: Django or FastAPI

*Front-end*: Javascript

*Back-end*: Python

*Database*: Postgres

*Testing*: Jest, Playright, Pytest, Nose, Jasmine, Selenium

**Sprint 1**

**Goal:** Research and AWS Setup

**Scrum Leader:** Rexford Essilfie

**Product Owner:** Ryan Edwall

Tasks:
- [x] Create a mock python script that outputs JSON for 20 steps [#12](https://github.com/sep-23/team_03/issues/12)
- [x] Research AWS RDS and relational database options [#7](https://github.com/sep-23/team_03/issues/7)
- [x] Research schema validation [#9](https://github.com/sep-23/team_03/issues/9)
- [x] Gain AWS access [#13](https://github.com/sep-23/team_03/issues/13)
- [x] Generate user flows for the web app [#37](https://github.com/sep-23/team_03/issues/37)
- [x] Set up repo structure with PR templates [#14](https://github.com/sep-23/team_03/issues/14)
- [x] Research potential tech stacks for web app that can dynamically add fields [#10](https://github.com/sep-23/team_03/issues/10)[ #27](https://github.com/sep-23/team_03/issues/27)
- [x] Formulate schema data points and backend layout [#8](https://github.com/sep-23/team_03/issues/8)[ #11](https://github.com/sep-23/team_03/issues/11)
- [x] Formulate a testing plan [#40](https://github.com/sep-23/team_03/issues/40)
- [x] Identify use cases [#26](https://github.com/sep-23/team_03/issues/26)


