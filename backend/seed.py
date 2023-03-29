# Cache for Created Entities
users = {}
jobs = {}
events = {}


def seed_users(db):
    print("Seeding Users")
    from app import models
    from app.internal import get_password_hash

    users_data = [
        # Customers
        dict(email="johndoe@gmail.com", password="abc"),
        dict(email="janeblack@gmail.com", password="abc"),
        # Providers
        dict(email="noodlesco@gmail.com", password="abc"),
        dict(email="botimage@gmail.com", password="abc"),
    ]

    for data in users_data:
        print(f"  Seeding user: {str(data)}")
        user = models.User(
            email=data["email"], hashed_password=get_password_hash(data["password"])
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        users[user.email] = user


def seed_jobs(db):
    print("Seeding Jobs")
    from app import models

    jobs_data = [
        # Job 1
        dict(
            customer_email="johndoe@gmail.com",
            provider_email="botimage@gmail.com",
            provider_job_id="botimage-123",
            provider_job_name="KidneyV1",
        ),
        # Job 2
        dict(
            customer_email="janeblack@gmail.com",
            provider_email="botimage@gmail.com",
            provider_job_id="noodlesco-123",
            provider_job_name="LungsV3",
        ),
    ]

    for data in jobs_data:
        print(f"  Seeding job {str(data)}")
        customer_id = users[data["customer_email"]].id
        provider_id = users[data["provider_email"]].id

        job = models.Job(
            customer_id=customer_id,
            provider_id=provider_id,
            provider_job_name=data["provider_job_name"],
            provider_job_id=data["provider_job_id"],
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        jobs[job.provider_job_id] = job


def seed_events(db):
    print("Seeding Events")
    from app import models

    events_data = [
        #  Job 1, Event 1
        dict(
            provider_job_id="botimage-123",
            kind="step",
            name="Scanning Left Kidney",
        ),
        #  Job 1, Event 2
        dict(
            provider_job_id="botimage-123",
            kind="step",
            name="Scanning Right Kidney",
        ),
        #  Job 1, Event 3
        dict(
            provider_job_id="botimage-123",
            kind="step",
            name="Analyze Kidney Results",
        ),
        #  Job 2, Event 1
        dict(
            provider_job_id="noodlesco-123",
            kind="step",
            name="Scanning Left Lung",
        ),
        #  Job 2, Event 2
        dict(
            provider_job_id="noodlesco-123",
            kind="step",
            name="Scanning Right Lung",
        ),
        #  Job 2, Event 3
        dict(
            provider_job_id="noodlesco-123",
            kind="step",
            name="Analyze Lung Results",
        ),
    ]

    for data in events_data:
        print(f"  Seeding event: {str(data)}")

        job = jobs[data["provider_job_id"]]

        event = models.Event(
            job_id=job.id,
            kind=data["kind"],
            name=data["name"],
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        events[event.id] = event


def seed_db():
    from config.database import SessionLocal

    db = SessionLocal()
    seed_users(db)
    seed_jobs(db)
    seed_events(db)
