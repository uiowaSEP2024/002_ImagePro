from app import models
from app.internal import get_password_hash
from app.schemas.user import UserRoleEnum
from config import config
from sqlalchemy import event, inspect


@event.listens_for(models.JobConfiguration, "init")
@event.listens_for(models.StepConfiguration, "init")
def create_nested(target, args, kwargs):
    """
    Source = https://stackoverflow.com/a/45911439
    """
    for rel in inspect(target.__class__).relationships:
        rel_cls = rel.mapper.class_

        if rel.key in kwargs:
            kwargs[rel.key] = [rel_cls(**c) for c in kwargs[rel.key]]


# Cache for Created Entities
users = {}
jobs = {}
events = {}
api_keys = {}
job_configs = {}

# Data to be seeded for each entity
USERS_DATA = [
    # Customers
    dict(
        email="johndoe@gmail.com",
        password="abcdefg",
        first_name="John",
        last_name="Doe",
        role=UserRoleEnum.customer,
    ),
    dict(
        email="janeblack@gmail.com",
        password="abcdefg",
        first_name="Jane",
        last_name="Black",
        role=UserRoleEnum.customer,
    ),
    # Providers
    dict(
        email="noodlesco@gmail.com",
        password="abcdefg",
        first_name="NoodlesCo",
        role=UserRoleEnum.provider,
    ),
    dict(
        email="botimage@gmail.com",
        password="abcdefg",
        first_name="BotImage",
        role=UserRoleEnum.provider,
    ),
]

API_KEYS_DATA = [
    # Providers
    dict(
        email="noodlesco@gmail.com",
        key="VCm4-RBXxgtg__yqxf0SYGLHGn8",
        note="Noodles & Co Key",
    ),
    dict(
        email="botimage@gmail.com",
        key="q-jAqPWCRGr2u6SeK6r6U0LBfJA",
        note="Bot Image Key",
    ),
]


JOBS_CONFIGURATIONS = [
    dict(
        name="Kidney Cancer",
        version="1.0.0",
        tag="kidney_cancer",
        provider_email="botimage@gmail.com",
        step_configurations=[
            dict(
                name="Left Kidney",
                tag="kidney_left",
                points=15,
                metadata_configurations=[
                    dict(name="Protein Density", units="gm/cc", kind="number"),
                    dict(name="Opacity", units="%", kind="number"),
                    dict(name="Color", kind="text"),
                    dict(name="Report", kind="link"),
                ],
            ),
            dict(
                name="Right Kidney",
                tag="kidney_right",
                points=15,
                metadata_configurations=[
                    dict(name="Protein Density", units="gm/cc", kind="number"),
                    dict(name="Opacity", units="%", kind="number"),
                    dict(name="Color", kind="text"),
                    dict(name="Report", kind="link"),
                ],
            ),
            dict(
                name="Kidney Results",
                tag="kidney_results",
                points=10,
                metadata_configurations=[dict(name="Verdict", kind="text")],
            ),
        ],
    ),
    dict(
        name="Heart Cancer",
        version="1.0.0",
        tag="heart_cancer",
        provider_email="botimage@gmail.com",
        step_configurations=[
            dict(
                name="Left Heart",
                tag="heart_left",
                points=15,
                metadata_configurations=[
                    dict(name="Protein Density", units="gm/cc", kind="number"),
                    dict(name="Opacity", units="%", kind="number"),
                    dict(name="Color", kind="text"),
                    dict(name="Report", kind="link"),
                ],
            ),
            dict(
                name="Right Heart",
                tag="heart_right",
                points=15,
                metadata_configurations=[
                    dict(name="Protein Density", units="gm/cc", kind="number"),
                    dict(name="Opacity", units="%", kind="number"),
                    dict(name="Color", kind="text"),
                    dict(name="Report", kind="link"),
                ],
            ),
            dict(
                name="Heart Results",
                tag="heart_results",
                points=10,
                metadata_configurations=[dict(name="Verdict", kind="text")],
            ),
        ],
    ),
    dict(
        name="Pancreas Cancer",
        version="1.0.0",
        tag="pancreas_cancer",
        provider_email="botimage@gmail.com",
        step_configurations=[
            dict(
                name="Left Pancreas",
                tag="pancreas_results",
                points=15,
                metadata_configurations=[
                    dict(name="Protein Density", units="gm/cc", kind="number"),
                    dict(name="Opacity", units="%", kind="number"),
                    dict(name="Color", kind="text"),
                    dict(name="Report", kind="link"),
                ],
            ),
        ],
    ),
    dict(
        name="Lung Cancer",
        version="1.0.0",
        tag="lung_cancer",
        provider_email="noodlesco@gmail.com",
        step_configurations=[
            dict(
                name="Left Lung",
                tag="left_lung",
                points=15,
                metadata_configurations=[
                    dict(name="Protein Density", units="gm/cc", kind="number"),
                    dict(name="Opacity", units="%", kind="number"),
                    dict(name="Color", kind="text"),
                    dict(name="Report", kind="link"),
                ],
            ),
            dict(
                name="Right Lung",
                tag="right_lung",
                points=15,
                metadata_configurations=[
                    dict(name="Protein Density", units="gm/cc", kind="number"),
                    dict(name="Opacity", units="%", kind="number"),
                    dict(name="Color", kind="text"),
                    dict(name="Report", kind="link"),
                ],
            ),
            dict(
                name="Lung Results",
                tag="lung_results",
                points=10,
                metadata_configurations=[dict(name="Verdict", kind="text")],
            ),
        ],
    ),
]


JOBS_DATA = [
    # Job 1 John
    dict(
        customer_email="johndoe@gmail.com",
        provider_email="botimage@gmail.com",
        provider_job_id="botimage-123",
        job_configuration_tag="lung_cancer",
    ),
    # Job 2 John
    dict(
        customer_email="johndoe@gmail.com",
        provider_email="botimage@gmail.com",
        provider_job_id="botimage-456",
        job_configuration_tag="heart_cancer",
    ),
    # Job 3 John
    dict(
        customer_email="johndoe@gmail.com",
        provider_email="botimage@gmail.com",
        provider_job_id="botimage-789",
        job_configuration_tag="pancreas_cancer",
    ),
    # Job 1 Jane
    dict(
        customer_email="janeblack@gmail.com",
        provider_email="noodlesco@gmail.com",
        provider_job_id="noodlesco-123",
        job_configuration_tag="lung_cancer",
    ),
]

EVENTS_DATA = [
    #  Job 1 John, Event 1
    dict(
        provider_job_id="botimage-123",
        kind="Pending",
        job_configuration_tag="kidney_cancer",
        step_configuration_tag="kidney_left",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Job 1 John, Event 2
    dict(
        provider_job_id="botimage-123",
        kind="Pending",
        job_configuration_tag="kidney_cancer",
        step_configuration_tag="kidney_right",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Job 1 John, Event 3
    dict(
        provider_job_id="botimage-123",
        kind="Complete",
        job_configuration_tag="kidney_cancer",
        step_configuration_tag="kidney_results",
        event_metadata={
            "Verdict": "Negative",
        },
    ),
    #  Job 2 John, Event 1
    dict(
        provider_job_id="botimage-456",
        kind="Pending",
        job_configuration_tag="heart_cancer",
        step_configuration_tag="heart_left",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Job 2 John, Event 2
    dict(
        provider_job_id="botimage-456",
        kind="Pending",
        job_configuration_tag="heart_cancer",
        step_configuration_tag="heart_right",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Job 2 John, Event 3
    dict(
        provider_job_id="botimage-456",
        kind="Complete",
        job_configuration_tag="heart_cancer",
        step_configuration_tag="heart_results",
        event_metadata={
            "Verdict": "Negative",
        },
    ),
    #  Job 3 John, Event 1
    dict(
        provider_job_id="botimage-789",
        kind="Complete",
        job_configuration_tag="pancreas_cancer",
        step_configuration_tag="pancreas_results",
        event_metadata={
            "Verdict": "Negative",
        },
    ),
    #  Job 1 Jane, Event 1
    dict(
        provider_job_id="noodlesco-123",
        kind="Pending",
        job_configuration_tag="lung_cancer",
        step_configuration_tag="left_lung",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Job 1 Jane, Event 2
    dict(
        provider_job_id="noodlesco-123",
        kind="Pending",
        job_configuration_tag="lung_cancer",
        step_configuration_tag="right_lung",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Job 1 Jane, Event 3
    dict(
        provider_job_id="noodlesco-123",
        kind="Complete",
        job_configuration_tag="lung_cancer",
        step_configuration_tag="lung_results",
        event_metadata={
            "Verdict": "Negative",
        },
    ),
]


def seed_users(db):
    print("Seeding Users")

    for user_data in USERS_DATA:
        print(f"  Seeding user: {str(user_data)}")
        user = models.User(
            email=user_data["email"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
            hashed_password=get_password_hash(user_data["password"]),
            role=user_data["role"],
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
            user_id=user.id, key=api_key_data["key"], note=api_key_data["note"]
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
        job_config = job_configs[job_data["job_configuration_tag"]]

        job = models.Job(
            customer_id=customer.id,
            provider_id=provider.id,
            job_configuration_id=job_config.id,
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
        job_config = job_configs[event_data["job_configuration_tag"]]
        step_config = [
            x
            for x in job_config.step_configurations
            if x.tag == event_data["step_configuration_tag"]
        ][0]

        event = models.Event(
            job_id=job.id,
            kind=event_data["kind"],
            step_configuration_id=step_config.id,
            event_metadata=event_data.get("event_metadata", None),
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        events[event.id] = event


def seed_job_configurations(db):
    print("Seeding Job Configurations")
    from app import models

    for job_config_data in JOBS_CONFIGURATIONS:
        print(f"  Seeding job configuration: {str(job_config_data)}")
        user = users[job_config_data.pop("provider_email")]

        job_config = models.JobConfiguration(**job_config_data, provider_id=user.id)

        db.add(job_config)
        db.commit()
        db.refresh(job_config)

        job_configs[job_config.tag] = job_config


def seed_db():
    db = config.db.SessionLocal()
    seed_users(db)
    seed_api_keys(db)
    seed_job_configurations(db)
    seed_jobs(db)
    seed_events(db)
