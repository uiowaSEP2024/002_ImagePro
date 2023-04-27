---
sidebar_position: 2
---

# Database Structure

This is how are database is currently structured.

## Entities

There are currently five entities in our database that support the application. All these entities have certain common fields such as `id`, `created_at` and `updated_at` which keep track of changes using timestamps.

1. `Users`
2. `Events`
3. `Jobs`
4. `Tokens`
5. `API-Keys`

## Users

There are two types of users considered by our application: **customers** and **providers**.
The Columns associated with the entity:

1. `role` : It is an enum that dictates whether a user is a customer or a provider.
2. `email` : The email ID of the user used at login.
3. `password` : The password that the user creates on signup and uses at login.
4. `first_name` : The first name of the user.
5. `last_name` : The last name of the user.

## Events
