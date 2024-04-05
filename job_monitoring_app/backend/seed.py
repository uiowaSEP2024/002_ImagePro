from app import models
from app import services
from app.internal import get_password_hash
from app.schemas.user import UserRoleEnum
from config import config
from sqlalchemy import event, inspect
from app.schemas.user import UserHospitalCreate
from app.schemas.user import UserProviderCreate
from app.schemas.user import UserCreate


@event.listens_for(models.StudyConfiguration, "init")
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
study_configs = {}
studies = {}
events = {}
hospitals = {}
providers = {}
users = {}
api_keys = {}

# Data to be seeded for each entity
STUDIES_CONFIGURATIONS = [
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


STUDIES_DATA = [
    # study 1 John
    dict(
        hospital_email="johndoe@gmail.com",
        provider_email="botimage@gmail.com",
        provider_study_id="botimage-123",
        study_configuration_tag="lung_cancer",
    ),
    # study 2 John
    dict(
        hospital_email="johndoe@gmail.com",
        provider_email="botimage@gmail.com",
        provider_study_id="botimage-456",
        study_configuration_tag="heart_cancer",
    ),
    # study 3 John
    dict(
        hospital_email="johndoe@gmail.com",
        provider_email="botimage@gmail.com",
        provider_study_id="botimage-789",
        study_configuration_tag="pancreas_cancer",
    ),
    # study 1 Jane
    dict(
        hospital_email="janeblack@gmail.com",
        provider_email="noodlesco@gmail.com",
        provider_study_id="noodlesco-123",
        study_configuration_tag="lung_cancer",
    ),
]

EVENTS_DATA = [
    #  Study 1 John, Event 1
    dict(
        provider_study_id="botimage-123",
        kind="Pending",
        study_configuration_tag="kidney_cancer",
        step_configuration_tag="kidney_left",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Study 1 John, Event 2
    dict(
        provider_study_id="botimage-123",
        kind="Pending",
        study_configuration_tag="kidney_cancer",
        step_configuration_tag="kidney_right",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Study 1 John, Event 3
    dict(
        provider_study_id="botimage-123",
        kind="Complete",
        study_configuration_tag="kidney_cancer",
        step_configuration_tag="kidney_results",
        event_metadata={
            "Verdict": "Negative",
        },
    ),
    #  Study 2 John, Event 1
    dict(
        provider_study_id="botimage-456",
        kind="Pending",
        study_configuration_tag="heart_cancer",
        step_configuration_tag="heart_left",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Study 2 John, Event 2
    dict(
        provider_study_id="botimage-456",
        kind="Pending",
        study_configuration_tag="heart_cancer",
        step_configuration_tag="heart_right",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Study 2 John, Event 3
    dict(
        provider_study_id="botimage-456",
        kind="Complete",
        study_configuration_tag="heart_cancer",
        step_configuration_tag="heart_results",
        event_metadata={
            "Verdict": "Negative",
        },
    ),
    #  Study 3 John, Event 1
    dict(
        provider_study_id="botimage-789",
        kind="Complete",
        study_configuration_tag="pancreas_cancer",
        step_configuration_tag="pancreas_results",
        event_metadata={
            "Verdict": "Negative",
        },
    ),
    #  Study 1 Jane, Event 1
    dict(
        provider_study_id="noodlesco-123",
        kind="Pending",
        study_configuration_tag="lung_cancer",
        step_configuration_tag="left_lung",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Study 1 Jane, Event 2
    dict(
        provider_study_id="noodlesco-123",
        kind="Pending",
        study_configuration_tag="lung_cancer",
        step_configuration_tag="right_lung",
        event_metadata={
            "Protein Density": 50,
            "Opacity": 0.9,
            "Report": "http://wwbp.org/papers/PsychSci2015_HeartDisease.pdf",
            "Color": "Lime Pink",
        },
    ),
    #  Study 1 Jane, Event 3
    dict(
        provider_study_id="noodlesco-123",
        kind="Complete",
        study_configuration_tag="lung_cancer",
        step_configuration_tag="lung_results",
        event_metadata={
            "Verdict": "Negative",
        },
    ),
]

HOSPITALS_DATA = [
    dict(
        hospital_name="John's Hospital",
    ),
    dict(
        hospital_name="Jane's Hospital",
    ),
]

PROVIDERS_DATA = [
    dict(
        provider_name="BotImage",
    ),
    dict(
        provider_name="NoodlesCo",
    ),
]

USERS_DATA = [
    # Hospital users
    dict(
        email="johndoe@gmail.com",
        password="abcdefg",
        first_name="John",
        last_name="Doe",
        role=UserRoleEnum.hospital,
        hospital_id=1,
    ),
    dict(
        email="janeblack@gmail.com",
        password="abcdefg",
        first_name="Jane",
        last_name="Black",
        role=UserRoleEnum.hospital,
        hospital_id=2,
    ),
    # Providers
    dict(
        email="noodlesco@gmail.com",
        password="abcdefg",
        first_name="NoodlesCo user",
        role=UserRoleEnum.provider,
        provider_id=2,
    ),
    dict(
        email="botimage@gmail.com",
        password="abcdefg",
        first_name="BotImage user",
        role=UserRoleEnum.provider,
        provider_id=1,
    ),
    # Admins
    dict(
        email="admin1@admin.com",
        password="abcdefg",
        first_name="Admin1",
        role=UserRoleEnum.admin,
    ),
    dict(
        email="admin2@admin.com",
        password="abcdefg",
        first_name="Admin2",
        role=UserRoleEnum.admin,
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

        if user.role == UserRoleEnum.hospital:
            input = {
                "email": user_data["email"],
                "first_name": user_data.get("first_name", ""),
                "last_name": user_data.get("last_name", ""),
                "password": user_data["password"],
                "role": user_data["role"],
                "hospital_id": user_data.get("hospital_id", None),
            }
            db_user = services.create_hospital_user(
                db, UserHospitalCreate.parse_obj(input)
            )

        elif user.role == UserRoleEnum.provider:
            input = {
                "email": user_data["email"],
                "first_name": user_data.get("first_name", ""),
                "last_name": user_data.get("last_name", ""),
                "password": user_data["password"],
                "role": user_data["role"],
                "provider_id": user_data.get("provider_id", None),
            }
            db_user = services.create_provider_user(
                db, UserProviderCreate.parse_obj(input)
            )
        else:
            input = {
                "email": user_data["email"],
                "first_name": user_data.get("first_name", ""),
                "last_name": user_data.get("last_name", ""),
                "password": user_data["password"],
                "role": user_data["role"],
            }
            db_user = services.create_user(db, UserCreate.parse_obj(input))

        users[user.email] = db_user


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


def seed_studies(db):
    print("Seeding Studies")
    from app import models

    for study_data in STUDIES_DATA:
        print(f"  Seeding study {str(study_data)}")
        user_hospital = users[study_data["hospital_email"]]
        user_provider = users[study_data["provider_email"]]
        study_config = study_configs[study_data["study_configuration_tag"]]

        study = models.Study(
            hospital_id=services.get_user_hospital(db, user_hospital.id).id,
            provider_id=services.get_user_provider(db, user_provider.id).id,
            study_configuration_id=study_config.id,
            provider_study_id=study_data["provider_study_id"],
        )

        db.add(study)
        db.commit()
        db.refresh(study)

        studies[study.provider_study_id] = study


def seed_events(db):
    print("Seeding Events")
    from app import models

    for event_data in EVENTS_DATA:
        print(f"  Seeding event: {str(event_data)}")

        study = studies[event_data["provider_study_id"]]
        study_config = study_configs[event_data["study_configuration_tag"]]
        step_config = [
            x
            for x in study_config.step_configurations
            if x.tag == event_data["step_configuration_tag"]
        ][0]

        event = models.Event(
            study_id=study.id,
            kind=event_data["kind"],
            step_configuration_id=step_config.id,
            event_metadata=event_data.get("event_metadata", None),
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        events[event.id] = event


def seed_study_configurations(db):
    print("Seeding Study Configurations")
    from app import models

    for study_config_data in STUDIES_CONFIGURATIONS:
        print(f"  Seeding study configuration: {str(study_config_data)}")
        user = users[study_config_data.pop("provider_email")]
        provider = services.get_provider_by_user_id(db, user.id)

        study_config = models.StudyConfiguration(
            **study_config_data, provider_id=provider.id
        )

        db.add(study_config)
        db.commit()
        db.refresh(study_config)

        study_configs[study_config.tag] = study_config


def seed_hospitals(db):
    print("Seeding Hospitals")
    from app import models

    for hospital_data in HOSPITALS_DATA:
        print(f"  Seeding hospital: {str(hospital_data)}")
        hospital = models.Hospital(**hospital_data)
        db.add(hospital)
        db.commit()
        db.refresh(hospital)

        hospitals[hospital.id] = hospital


def seed_providers(db):
    print("Seeding Providers")
    from app import models

    for provider_data in PROVIDERS_DATA:
        print(f"  Seeding provider: {str(provider_data)}")
        provider = models.Provider(**provider_data)
        db.add(provider)
        db.commit()
        db.refresh(provider)

        providers[provider.id] = provider


def seed_db():
    db = config.db.SessionLocal()
    seed_hospitals(db)
    seed_providers(db)
    seed_users(db)
    seed_api_keys(db)
    seed_study_configurations(db)
    seed_studies(db)
    seed_events(db)
