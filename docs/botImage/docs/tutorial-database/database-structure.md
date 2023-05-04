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
2. `provider_job_id` : This is the provider that is associated to the event.

## API-Keys

The columns associated with the entity:

1. `user_id` : The user that is associated to the API Key.
2. `key` : The random secret string that represents the API Key.
3. `note` : The description of the API Key.
