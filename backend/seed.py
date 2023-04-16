from config import config

# Cache for Created Entities
users = {}
jobs = {}
events = {}
api_keys = {}

# Data to be seeded for each entity
USERS_DATA = [
    # Customers
    dict(email="johndoe@gmail.com", password="abc", first_name="John", last_name="Doe"),
    dict(
        email="janeblack@gmail.com",
        password="abc",
        first_name="Jane",
        last_name="Black",
    ),
    # Providers
    dict(email="noodlesco@gmail.com", password="abc", first_name="NoodlesCo"),
    dict(email="botimage@gmail.com", password="abc", first_name="BotImage"),
]

API_KEYS_DATA = [
    # Providers
    dict(email="noodlesco@gmail.com", key="VCm4-RBXxgtg__yqxf0SYGLHGn8"),
    dict(email="botimage@gmail.com", key="q-jAqPWCRGr2u6SeK6r6U0LBfJA"),
]

JOBS_DATA = [
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

EVENTS_DATA = [
    #  Job 1, Event 1
    dict(
        provider_job_id="botimage-123",
        kind="step",
        name="Scanning Left Kidney",
        event_metadata={
            "official": "Yes"
        }
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
        kind="complete",
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
        kind="complete",
        name="Analyze Lung Results",
    ),
]


def seed_users(db):
    print("Seeding Users")
    from app import models
    from app.internal import get_password_hash

    for user_data in USERS_DATA:
        print(f"  Seeding user: {str(user_data)}")
        user = models.User(
            email=user_data["email"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
            hashed_password=get_password_hash(user_data["password"]),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        users[user.email] = user


def seed_api_keys(db):
    print("Seeding Api Keys")
    from app import models

    for api_key_data in API_KEYS_DATA:
        print(f"  Seeding api key: {str(api_key_data)}")
        user = users[api_key_data["email"]]
        api_key = models.Apikey(
            user_id=user.id,
            key=api_key_data["key"],
        )
        db.add(api_key)
        db.commit()
        db.refresh(api_key)

        api_keys[api_key.id] = api_key


def seed_jobs(db):
    print("Seeding Jobs")
    from app import models

    for job_data in JOBS_DATA:
        print(f"  Seeding job {str(job_data)}")
        customer = users[job_data["customer_email"]]
        provider = users[job_data["provider_email"]]

        job = models.Job(
            customer_id=customer.id,
            provider_id=provider.id,
            provider_job_name=job_data["provider_job_name"],
            provider_job_id=job_data["provider_job_id"],
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        jobs[job.provider_job_id] = job


def seed_events(db):
    print("Seeding Events")
    from app import models

    for event_data in EVENTS_DATA:
        print(f"  Seeding event: {str(event_data)}")

        job = jobs[event_data["provider_job_id"]]

        event = models.Event(
            job_id=job.id,
            kind=event_data["kind"],
            name=event_data["name"],
            event_metadata=event_data.get("event_metadata", None)
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        events[event.id] = event


def seed_db():
    db = config.db.SessionLocal()
    seed_users(db)
    seed_api_keys(db)
    seed_jobs(db)
    seed_events(db)
