---
sidebar_position: 3
---

# Deploy your Frontend

Learn how to deploy the frontend to **AWS**.

### AWS Console

1. Ensure you have an AWS account. Sign in to the AWS management console and access the **Amplify** console.
2. You will see two options: **Amplify Studio** and **Amplify Hosting**. Press `Get Started` under the **Amplify Hosting** subheading.

### Connecting Repository

1. Select your code provider (**Note:** Select your file is also an option if you wish to locally add files). Since we are using Github to work on the project, select **Github** from the options.
2. The browser then should redirect you to the Github website and ask for certain permissions. All of these are standard read-only permissions and should be granted.
3. After providing the permissions, the browser should again be redirected to the Amplify console.
4. You will then be asked to select a repository from the dropdown menu. Select the appropriate repository.
5. Then, select the branch of the repository that would be the source of the deployment.
6. Notice that the repository has a lot of different components (Ex - Backend, Frontend, etc). Since we are hosting only the frontend, we will have to select the checkbox **Connecting a monorepo? Pick a folder.**.
7. We then provide the path of the required folder. In our case, it should just be **frontend**.

### Build Settings

1. Choose an application name for the deployed application. This will be visible on your Amplify console.
2. Amplify will then generate a `.yml` file that contains the deployment settings. Ensure that appRoot points to frontend.
3. The app requires an IAM service role that Amplify assumes when calling other services on your behalf.
4. There are two options: using an exising IAM role or creating a new one.
5. If creating a new role, choose **Create and use a new service role**
6. If using a previously defined role, choose **Use an existing service role** and then select the role from the list.
7. The next step would be to review the deployment details and if everything is in order, then select **Save and Deploy**.

### Learn More

- [AWS Documentation](https://docs.aws.amazon.com/amplify/latest/userguide/deploy-nextjs-app.html) - Read on using AWS Amplify for deploynment.
