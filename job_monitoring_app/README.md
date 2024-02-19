**Team 03 README**

**Team Members:** Himanshu Bainwala, Rexford Essilfie, Ryan Edwall, Anand Gopalakrishnan, and Mira Tellegen

**Client:** Professor Hans Johnson

**Project:** BotImage, an AWS RDS which accepts JSON output from a python script in a VPC, validates the schema, and catalogs progress and billing through a variable and extensible number of steps. Accompanied by a web app where clients and admin can view jobs, job progress, and billing.

**Quick-Start**<br/>
Documentation overview: [https://github.com/sep-23/team_03/wiki/User-Manual](https://github.com/sep-23/team_03/wiki/User-Manual)

**Meeting Schedule**

Stand ups: Monday 11:30am, Tuesday 7pm, Wednesday 11:30am, Thursday 7pm, Friday 11:30am, Sunday 7pm

Client Meetings: Monday 11:00am

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

*Framework*: FastAPI

*Front-end*: Javascript

*Back-end*: Python

*Database*: Postgres

*Testing*: Jest, Pytest
**Sprint 1**

**Goal:** Research and AWS Setup

**Scrum Leader:** Rexford Essilfie

**Product Owner:** Ryan Edwall

**Points Completed** 32

Research Tasks:
- [x] Research AWS RDS and relational database options [#7](https://github.com/sep-23/team_03/issues/7)
- [x] Research schema validation [#9](https://github.com/sep-23/team_03/issues/9)
- [x] Research potential tech stacks for web app that can dynamically add fields [#10](https://github.com/sep-23/team_03/issues/10)[ #27](https://github.com/sep-23/team_03/issues/27)

Tasks:
- [x] Formulate schema data points and backend layout [#8](https://github.com/sep-23/team_03/issues/8)[#11](https://github.com/sep-23/team_03/issues/11)
- [x] Create a mock python script that outputs JSON for 20 steps [#12](https://github.com/sep-23/team_03/issues/12)
- [x] Gain AWS access [#13](https://github.com/sep-23/team_03/issues/13)
- [x] Set up repo structure with PR templates [#14](https://github.com/sep-23/team_03/issues/14)
- [x] Identify use cases [#26](https://github.com/sep-23/team_03/issues/26)
- [x] Generate user flows for the web app [#37](https://github.com/sep-23/team_03/issues/37)
- [x] Formulate a testing plan [#40](https://github.com/sep-23/team_03/issues/40)
- [x] Create sample AWS Databases [#42](https://github.com/sep-23/team_03/issues/42)

<img width="1028" alt="Screen Shot 2023-04-29 at 5 33 48 PM" src="https://user-images.githubusercontent.com/64100162/235326860-44eba878-5b7e-4e15-9834-78dc88050cb9.png">


**Sprint 2**

**Goal:** Frontend and Backend Setup, User Authentication

**Scrum Leader:** Rexford Essilfie

**Product Owner:** Ryan Edwall

**Points Completed:** 30

Tasks:

- [x] Continuous Integration [#15](https://github.com/sep-23/team_03/issues/15)
- [x] Prototype for job configurations [#44](https://github.com/sep-23/team_03/issues/44)
- [x] Experiment with sample AWS lambda [#45](https://github.com/sep-23/team_03/issues/45)
- [x] Setup frontend [#48](https://github.com/sep-23/team_03/issues/48)
- [x] Account creation and login [#50](https://github.com/sep-23/team_03/issues/53), [#18](https://github.com/sep-23/team_03/issues/54)
- [x] Setup frontend and backend code linters [#53](https://github.com/sep-23/team_03/issues/53), [#54](https://github.com/sep-23/team_03/issues/54)
- [x] Deploy backend and frontend [#52](https://github.com/sep-23/team_03/issues/52), [#55](https://github.com/sep-23/team_03/issues/55)
- [x] Setup database migrations [#56](https://github.com/sep-23/team_03/issues/56)
- [x] Setup backend [#61](https://github.com/sep-23/team_03/issues/61), [#51](https://github.com/sep-23/team_03/issues/51)
- [x] Secure access to backend [#57](https://github.com/sep-23/team_03/issues/57)

<img width="1022" alt="Screen Shot 2023-04-29 at 5 34 06 PM" src="https://user-images.githubusercontent.com/64100162/235326867-bee7c6ca-4548-4ed9-9b6a-a3d300984b28.png">


**Sprint 3**

**Goal:** Connecting Backend and Frontend, Jobs, AWS Configuration

**Scrum Leader:** Rexford Essilfie

**Product Owner:** Ryan Edwall

**Points Completed:** 28

Tasks:

- [x] README and user handbook [#17](https://github.com/sep-23/team_03/issues/17)
- [x] Authentication and protected routes [#19](https://github.com/sep-23/team_03/issues/19)
- [x] Progress bar on site [#20](https://github.com/sep-23/team_03/issues/20)
- [x] Jobs table search and filter [#21](https://github.com/sep-23/team_03/issues/21)
- [x] Extract column and job info from database [#46](https://github.com/sep-23/team_03/issues/46)
- [x] Show jobs data on frontend [#47](https://github.com/sep-23/team_03/issues/47)
- [x] Saving jobs in the database [#49](https://github.com/sep-23/team_03/issues/49)
- [x] User roles and personalized data display [#75](https://github.com/sep-23/team_03/issues/75)
- [x] Bash script to automate AWS setup [#76](https://github.com/sep-23/team_03/issues/76)

<img width="1022" alt="Screen Shot 2023-04-29 at 5 34 16 PM" src="https://user-images.githubusercontent.com/64100162/235326872-352452e4-bf90-46ac-bb65-cfd5cc5e9490.png">


**Sprint 4**

**Goal:** Tracker API, Database, Seeding

**Scrum Leader:** Rexford Essilfie

**Product Owner:** Ryan Edwall

**Points Completed:** 23

Tasks:

- [x] Access to RDS from multiple environments [#77](https://github.com/sep-23/team_03/issues/77)
- [x] API Library to call in scripts for jobs [#95](https://github.com/sep-23/team_03/issues/95)
- [x] Script for backend authentication [#96](https://github.com/sep-23/team_03/issues/96)
- [x] API Library to call in scripts for events [#97](https://github.com/sep-23/team_03/issues/97)
- [x] Frontend to create API keys [#98](https://github.com/sep-23/team_03/issues/98)
- [x] Seeding database [#100](https://github.com/sep-23/team_03/issues/100)
- [x] Making calls to database for progress bar [#101](https://github.com/sep-23/team_03/issues/101)[#103](https://github.com/sep-23/team_03/issues/103)

<img width="1034" alt="Screen Shot 2023-04-29 at 5 34 23 PM" src="https://user-images.githubusercontent.com/64100162/235326884-caf12524-ef79-4119-919c-436a828efd8b.png">


**Sprint 5**

**Goal:** Errors, Job Configuration, UI Overhaul, Testing

**Scrum Leader:** Rexford Essilfie

**Product Owner:** Ryan Edwall

**Points Completed:** 29

Tasks:

- [x] Dynamically add data fields [#20](https://github.com/sep-23/team_03/issues/20)
- [x] Error tracking in job process [#23](https://github.com/sep-23/team_03/issues/23)
- [x] Weighting jobs [#113](https://github.com/sep-23/team_03/issues/113)
- [x] Specifications for job configuration [#114](https://github.com/sep-23/team_03/issues/114)
- [x] ChakraUI for Login [#121](https://github.com/sep-23/team_03/issues/121)
- [x] ChakraUI for Signup [#122](https://github.com/sep-23/team_03/issues/122)
- [x] API Table migration [#125](https://github.com/sep-23/team_03/issues/125)
- [x] ChakraUI for API Keys [#128](https://github.com/sep-23/team_03/issues/128)
- [x] ChakraUI for jobs [#131](https://github.com/sep-23/team_03/issues/131)
- [x] Job configuration files [#132](https://github.com/sep-23/team_03/issues/132)

<img width="1031" alt="Screen Shot 2023-04-29 at 5 34 30 PM" src="https://user-images.githubusercontent.com/64100162/235326886-731407ba-9685-42b4-9aa1-d9e915cd4a73.png">


**Sprint 6**

**Goal:** Analytics, Deployment, User Roles, Integration Testing

**Scrum Leader:** Rexford Essilfie

**Product Owner:** Ryan Edwall

**Points Completed:** 45

Tasks:

- [x] Job count analytics [#25](https://github.com/sep-23/team_03/issues/25)
- [x] Jobs search and filter [#28](https://github.com/sep-23/team_03/issues/28)
- [x] Persistent historical job info [#29](https://github.com/sep-23/team_03/issues/29)
- [x] Cost for steps and jobs [#30](https://github.com/sep-23/team_03/issues/30)
- [x] Aggregate step and error statistics [#32](https://github.com/sep-23/team_03/issues/32)
- [x] Aggregate usage per customer [#33](https://github.com/sep-23/team_03/issues/33)
- [x] Breadcrumbs for new user setup [#123](https://github.com/sep-23/team_03/issues/123)[#124](https://github.com/sep-23/team_03/issues/124)
- [x] Backend setup documentation [#126](https://github.com/sep-23/team_03/issues/126)
- [x] ChakraUI Documentation [#130](https://github.com/sep-23/team_03/issues/130)
- [x] Associate jobs and job configurations [#145](https://github.com/sep-23/team_03/issues/145)
- [x] Timestamps for jobs [#146](https://github.com/sep-23/team_03/issues/146)
- [x] Contact admin frontend link [#151](https://github.com/sep-23/team_03/issues/151)
- [x] Filling in professional UI [#151](https://github.com/sep-23/team_03/issues/152)
- [x] Frontend deployment [#153](https://github.com/sep-23/team_03/issues/153)

# Site Setup Documentation/Developer Guide

### Backend README
[https://github.com/sep-23/team_03/tree/main/backend](https://github.com/sep-23/team_03/tree/main/backend)

### Frontend README
[https://github.com/sep-23/team_03/tree/main/frontend](https://github.com/sep-23/team_03/tree/main/frontend)

### API README
[https://github.com/sep-23/team_03/tree/main/trackerapi](https://github.com/sep-23/team_03/tree/main/trackerapi)

### Our site developer documentation is navigable through [Docusaurus 2](https://docusaurus.io/)

Docusaurus README: [https://github.com/sep-23/team_03/tree/main/docs/botImage](https://github.com/sep-23/team_03/tree/main/docs/botImage)

## Access Developer Guide

To run docusaurus, you must have Node.js installed. Check if it is installed with

```
node -v
```

Then, clone the repository to your device with

```
git clone https://github.com/sep-23/team_03.git
```

Navigate to the documentation directory with

```
cd docs/botimage
```

Then, start the app with

```
npm run start
```

Navigate to [http://localhost:3000](http://localhost:3000) to explore developer documentation

If you want to add to the documentation or learn more about docusaurus, see their [getting started guide](https://docusaurus.io/docs/installation)

# Running App Locally

1. Clone the repository at [https://github.com/sep-23/team_03.git](https://github.com/sep-23/team_03.git)
2. `cd` into the frontend directory
3. Run `npm install` to install all the necessary dependencies
4. Run `npm run dev` to start the application in dev mode
5. Open the [http://localhost:3000](http://localhost:3000) url in your browser

## Running App Backend Locally

1. `cd` into the backend directory
2. Make sure you have Python installed (preferably v3.10), which you can download from [here](https://www.python.org/downloads/)
3. Before starting the application, make sure to create a virtual environment for the project:
   ```bash
   python -m venv .venv
   ```
4. Next, activate the virtual environment. **NB: You will have to do this step every time you start/open a fresh terminal**
   ```bash
   source venv/bin/activate
   ```
   > If you are working in PyCharm, steps 2 and 3 should be performed automatically for you.
   > Note the above may be .venv or venv depending on PyCharm

5. Once the virtual environment is started, make sure to install all requirements required for the project:
   ```bash
   pip install -r requirements.txt
   ```

6. Create a file called .env.local, and then copy and paste the contents from .env.example file
   into it, replacing with your own values as appropriate.

7. Next, we start a local database using Docker with the following script in a terminal:
   ```bash
   bash run-db.sh
   ```
   > If you get errors in this step, make sure you have installed docker first with `docker -v` in your terminal. If not,
   > you can download Docker [here](https://docs.docker.com/get-docker/).
   > If error 'Docker Daemon not running' is raised, then start the docker desktop application and try again.

8. Apply migrations to the database to set it up using the command:
   ```bash
   APP_ENV=development alembic upgrade head
   ```

9. Finally, to start the application, run the following script:
   ```bash
   bash run-dev.sh
   ```
10. You can manually run the app by running `uvicorn app.main:app --reload` in your terminal to run the Fast API service. In the case of an error, you may need to run `APP_ENV=development uvicorn app.main:app --reload`
11. To see users, run `uvicorn app.main:app --reload` in your terminal to run the Fast API service, navigate to [http://localhost:8000](http://localhost:8000), and add '/user'

# Bash Scripts

1. For running the app, from the backend directory, do `bash run-dev.sh`
2. For running tests, from the backend directory, do `bash run-tests.sh`

# Linters

The linters were designed using ESLint (frontend) and PyLama/PyCharm (backend)

## Frontend Linter

1. Run `npm install`
2. Run `npm run lint` to check warnings and errors for the styles
3. Run `npm run lint -- --fix` to fix the errors and warnings that are possible to be auto fixed

## Backend Linter

Documentation: [https://pypi.org/project/pylama/](https://pypi.org/project/pylama/)

1. Install requirements with `pip install -r requirements.txt`
2. Run `pylama <filename>` to use default linters for the specified filename
3. Alternatively, run `pylama -l <list of comma-separated linters> <filename>` to run a list of linters for the specified filepath (list method should only be used if linters don't need specific arguments, otherwise run them individually from cmd line)

### List of Useful Linters in Pylama Package
vulture - checks for dead code : [https://pypi.org/project/vulture/](https://pypi.org/project/vulture/) <br/>
eradicate - removes unused, commented out code: [https://pypi.org/project/eradicate/](https://pypi.org/project/eradicate/)<br/>
pylint - static code analyzer: [https://pypi.org/project/pylint/](https://pypi.org/project/pylint/)<br/>
pyflakes - similar to pylint but is faster and checks a smaller range of things: [https://pypi.org/project/pyflakes/](https://pypi.org/project/pyflakes/)<br/>
radon - computes difficulty and software quality metrics : [https://pypi.org/project/radon/](https://pypi.org/project/radon/)<br/>
mypy - checks type annotations: [https://pypi.org/project/mypy/](https://pypi.org/project/mypy/)<br/>
