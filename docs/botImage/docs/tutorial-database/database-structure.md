---
sidebar_position: 2
---

# Database Structure

This is how are database is currently structured.

## Entities

There are currently four entities in our database that support the application. All these entities have certain common fields such as `id`, `created_at` and `updated_at` which keep track of changes using timestamps.

1. `Users`
2. `Events`
3. `Jobs`
4. `API-Keys`
5. `Job Configurations`
6. `Step Configurations`
7. `Metadata Configurations`
8. `Alembic Version`

## Users

There are two types of users considered by our application: **customers** and **providers**.
The Columns associated with the entity:

1. `role` : It is an enum that dictates whether a user is a customer or a provider.
2. `email` : The email ID of the user used at login.
3. `password` : The password that the user creates on signup and uses at login.
4. `first_name` : The first name of the user.
5. `last_name` : The last name of the user.

## Events

The columns associated with the entity:

1. `kind` : It is an enum that dictates the type of the event among **step**, **error**, **info**, **complete**.
2. `job_id` : This is the job that is associated to the event.
3. `name` : This is the name of the event.
4. `step_configuration_id` : This is the step configuration that is associated with the event.
5. `event_metadata` : This is the metadata associated with the event.

## API-Keys

The columns associated with the entity:

1. `user_id` : The user that is associated to the API Key.
2. `key` : The random secret string that represents the API Key.
3. `note` : The description of the API Key.
4. `expires_at` : This denotes the date when the API key will expire.

## Jobs

The columns associated with the entity:

1. `provider_id` : This represents the provider that has issued the job.
2. `customer_id` : This represents the customer for whom the job was issued for.
3. `job_configuration_id` : This represents the configuration that is associated with the job.
4. `provider_job_id` : This represents the ID of the job issued by the provider.
5. `provider_job_name` : This represents the name of the job issued by the provider.

## Job Configurations

The columns associated with the entity:

1. `provider_id` : This represents the provider who is using this job configuration.
2. `tag` : This represents the unique tag for the job configuration.
3. `name` : This represents the name of the job.
4. `version` : This represents the version of the job configuration.

## Step Configurations

The columns associated with the entity:

1. `job_configuration_id` : This represents the job configuration that is associated with this step configuration.
2. `tag` : This represents the unique tag for the step configuration.
3. `name` : This represents the name of the step.
4. `points` : This represents the weighted points for the step.
