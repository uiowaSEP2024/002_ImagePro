---
sidebar_position: 3
---

# Deploy your Frontend

Learn how to deploy the frontend to **AWS**.

### AWS Console

- Ensure you have an AWS account. Sign in to the AWS management console and access the **Amplify** console.
- You will see two options: **Amplify Studio** and **Amplify Hosting**. Press `Get Started` under the **Amplify Hosting** subheading.

### Connecting Repository

- Select your code provider (**Note:** Select your file is also an option if you wish to locally add files). Since we are using Github to work on the project, select **Github** from the options.
- The browser then should redirect you to the Github website and ask for certain permissions. All of these are standard read-only permissions and should be granted.
- After providing the permissions, the browser should again be redirected to the Amplify console.
- You will then be asked to select a repository from the dropdown menu. Select the appropriate repository.
- Then, select the branch of the repository that would be the source of the deployment.
- Notice that the repository has a lot of different components (Ex - Backend, Frontend, etc). Since we are hosting only the frontend, we will have to select the checkbox **Connecting a monorepo? Pick a folder.**.
- We then provide the path of the required folder. In our case, it should just be **frontend**.

### Build Settings

### Learn More

- [AWS Documentation](https://docs.aws.amazon.com/amplify/latest/userguide/deploy-nextjs-app.html) - Read on using AWS Amplify for deploynment.
