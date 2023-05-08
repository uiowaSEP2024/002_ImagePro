---
sidebar_position: 4
---

# Seeding SQL Database

There is a seed file that generates dummy data for ease of testing purposes. Assuming that the database migrations were executed successfully and the database is up and running, the following command populates the database with the seeds.

```bash
python tasks.py db:dev:seed
```

The user information created by the seed file is in an incremental fashion so that there is no possibility of non-unique users being created.
