---
sidebar_position: 2
---

# Running the Frontend Locally

### Cloning the Repository

- The first step for running the frontend of the application is to clone the repository.

### Downloading the Necessary Libraries

- Open the terminal and notice the current path of the folder should be `team_03`
- Now that the team03 repository has been cloned, first navigate to the folder `/frontend` using the command `cd frontend`
- In the folder `/frontend`, notice the file `package.json` which contains information as what libraries are being used as well as different commands to run the frontend of the application.
- In the command line, run the command `npm install` or `npm i` to refer to the file `package.json` and download the necessary packages.

### Running the Application

- Now that all the necessary packages are installed, run the application locally by using the command `npm run dev` in the command line.
- Visit `http://localhost:3000` on your browser to view the application
- At this point, the application will not be accessible (the developer will not be able to login). To access the application read the tutorials titled `tutorial-backend/local-development` and `tutorial-database/local-development`.

### Testing the Application

- In order to run the linter (this project is using `ESLint`), open the terminal and run the command `npm run lint` to get the formatting differences
- In order to fix the formatting differences, run the command `npm run lint:fix` in the terminal
- In order to run the tests, run the command `npm run test` and view the statistics (total number of tests, number of passing tests and number of failing tests) in the terminal

### Learn More

- To learn more about Next.js, take a look at the following resources:
  - [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
  - [Learn Next.js](https://nextjs.org/learn/foundations/about-nextjs) - an inetractive Next.js tutorial.
