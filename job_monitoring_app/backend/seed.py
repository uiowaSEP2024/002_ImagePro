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
        version="0.0.1",
        name="Prostate Study",
        tag="prostate_study",
        provider_user_email="prostateimaginguser@gmail.com",
        step_configurations=[
            dict(name="Data Receiving", tag="data_receiving", points=1),
            dict(name="Data Download", tag="data_download", points=1),
            dict(name="Data Processing", tag="data_processing", points=1),
            dict(name="Data Return", tag="data_return", points=1),
        ],
    ),
    dict(
        version="0.0.1",
        name="Full Brain Study",
        tag="full_brain_study",
        provider_user_email="brainmaskuser@gmail.com",
        step_configurations=[
            dict(name="Data Receiving", tag="data_receiving", points=1),
            dict(name="Data Download", tag="data_download", points=1),
            dict(name="Data Processing", tag="data_processing", points=1),
            dict(name="Data Return", tag="data_return", points=1),
        ],
    ),
    dict(
        version="0.0.1",
        name="Cerebral Cortex Study",
        tag="cerebral_cortex_study",
        provider_user_email="brainmaskuser@gmail.com",
        step_configurations=[
            dict(name="Data Receiving", tag="data_receiving", points=1),
            dict(name="Data Download", tag="data_download", points=1),
            dict(name="Data Processing", tag="data_processing", points=1),
            dict(name="Data Return", tag="data_return", points=1),
        ],
    ),
    dict(
        version="0.0.1",
        name="Cerebellum Study",
        tag="cerebellum_study",
        provider_user_email="brainmaskuser@gmail.com",
        step_configurations=[
            dict(name="Data Receiving", tag="data_receiving", points=1),
            dict(name="Data Download", tag="data_download", points=1),
            dict(name="Data Processing", tag="data_processing", points=1),
            dict(name="Data Return", tag="data_return", points=1),
        ],
    ),
]

STUDIES_DATA = [
    # study 1 University Hospital
    dict(
        hospital_user_email="universityhospitaluser@gmail.com",
        provider_user_email="prostateimaginguser@gmail.com",
        provider_study_id="prostateimaging-123",
        study_configuration_tag="prostate_study",
    ),
    # study 2 Mercy Hospital
    dict(
        hospital_user_email="mercyhospitaluser@gmail.com",
        provider_user_email="brainmaskuser@gmail.com",
        provider_study_id="brainmask-456",
        study_configuration_tag="full_brain_study",
    ),
    # study 3 University Hospital
    dict(
        hospital_user_email="universityhospitaluser@gmail.com",
        provider_user_email="brainmaskuser@gmail.com",
        provider_study_id="brainmask-789",
        study_configuration_tag="cerebral_cortex_study",
    ),
    # study 4 University Hospital
    dict(
        hospital_user_email="universityhospitaluser@gmail.com",
        provider_user_email="brainmaskuser@gmail.com",
        provider_study_id="brainmask-123",
        study_configuration_tag="cerebellum_study",
    ),
]

EVENTS_DATA = [
    #  Study 1 University Hospital, Event 1
    dict(
        provider_study_id="prostateimaging-123",
        kind="Complete",
        study_configuration_tag="prostate_study",
        step_configuration_tag="data_receiving",
        event_metadata=dict(status="Complete"),
    ),
    #  Study 1 University Hospital, Event 2
    dict(
        provider_study_id="prostateimaging-123",
        kind="In progress",
        study_configuration_tag="prostate_study",
        step_configuration_tag="data_download",
        event_metadata=dict(status="In progress"),
    ),
    #  Study 1 University Hospital, Event 3
    dict(
        provider_study_id="prostateimaging-123",
        kind="Pending",
        study_configuration_tag="prostate_study",
        step_configuration_tag="data_processing",
        event_metadata=dict(status="Pending"),
    ),
    #  Study 1 University Hospital, Event 4
    dict(
        provider_study_id="prostateimaging-123",
        kind="Pending",
        study_configuration_tag="prostate_study",
        step_configuration_tag="data_return",
        event_metadata=dict(status="Pending"),
    ),
    #  Study 2 Mercy Hospital, Event 1
    dict(
        provider_study_id="brainmask-456",
        kind="Complete",
        study_configuration_tag="full_brain_study",
        step_configuration_tag="data_receiving",
        event_metadata=dict(status="Complete"),
    ),
    #  Study 2 Mercy Hospital, Event 2
    dict(
        provider_study_id="brainmask-456",
        kind="Complete",
        study_configuration_tag="full_brain_study",
        step_configuration_tag="data_download",
        event_metadata=dict(status="Complete"),
    ),
    #  Study 2 Mercy Hospital, Event 3
    dict(
        provider_study_id="brainmask-456",
        kind="In progress",
        study_configuration_tag="full_brain_study",
        step_configuration_tag="data_processing",
        event_metadata=dict(status="In progress"),
    ),
    #  Study 2 Mercy Hospital, Event 4
    dict(
        provider_study_id="brainmask-456",
        kind="Pending",
        study_configuration_tag="full_brain_study",
        step_configuration_tag="data_return",
        event_metadata=dict(status="Pending"),
    ),
    #  Study 3 University Hospital, Event 1
    dict(
        provider_study_id="brainmask-789",
        kind="Complete",
        study_configuration_tag="cerebral_cortex_study",
        step_configuration_tag="data_receiving",
        event_metadata=dict(status="Complete"),
    ),
    #  Study 3 University Hospital, Event 2
    dict(
        provider_study_id="brainmask-789",
        kind="Complete",
        study_configuration_tag="cerebral_cortex_study",
        step_configuration_tag="data_download",
        event_metadata=dict(status="Complete"),
    ),
    #  Study 3 University Hospital, Event 3
    dict(
        provider_study_id="brainmask-789",
        kind="Error",
        study_configuration_tag="cerebral_cortex_study",
        step_configuration_tag="data_processing",
        event_metadata=dict(status="Error"),
    ),
    #  Study 3 University Hospital, Event 4
    dict(
        provider_study_id="brainmask-789",
        kind="Pending",
        study_configuration_tag="cerebral_cortex_study",
        step_configuration_tag="data_return",
        event_metadata=dict(status="Pending"),
    ),
    #  Study 4 University Hospital, Event 1
    dict(
        provider_study_id="brainmask-123",
        kind="Complete",
        study_configuration_tag="cerebellum_study",
        step_configuration_tag="data_receiving",
        event_metadata=dict(status="Complete"),
    ),
    #  Study 4 University Hospital, Event 2
    dict(
        provider_study_id="brainmask-123",
        kind="Complete",
        study_configuration_tag="cerebellum_study",
        step_configuration_tag="data_download",
        event_metadata=dict(status="Complete"),
    ),
    #  Study 4 University Hospital, Event 3
    dict(
        provider_study_id="brainmask-123",
        kind="Complete",
        study_configuration_tag="cerebellum_study",
        step_configuration_tag="data_processing",
        event_metadata=dict(status="Complete"),
    ),
    #  Study 4 University Hospital, Event 4
    dict(
        provider_study_id="brainmask-123",
        kind="Complete",
        study_configuration_tag="cerebellum_study",
        step_configuration_tag="data_return",
        event_metadata=dict(status="Complete"),
    ),
]

HOSPITALS_DATA = [
    dict(
        hospital_name="University Hospital",
    ),
    dict(
        hospital_name="Mercy Hospital",
    ),
    dict(
        hospital_name="Unity Point Hospital",
    ),
]

PROVIDERS_DATA = [
    dict(
        provider_name="BrainMask",
    ),
    dict(
        provider_name="ProstateImaging",
    ),
]

USERS_DATA = [
    # Hospital users
    dict(
        email="universityhospitaluser@gmail.com",
        password="abcdefg",
        first_name="University Hospital user",
        role=UserRoleEnum.hospital,
        hospital_id=1,
    ),
    dict(
        email="mercyhospitaluser@gmail.com",
        password="abcdefg",
        first_name="Mercy Hospital user",
        last_name="Black",
        role=UserRoleEnum.hospital,
        hospital_id=2,
    ),
    # Providers
    dict(
        email="brainmaskuser@gmail.com",
        password="abcdefg",
        first_name="BrainMask user",
        role=UserRoleEnum.provider,
        provider_id=1,
    ),
    dict(
        email="prostateimaginguser@gmail.com",
        password="abcdefg",
        first_name="ProstateImaging user",
        role=UserRoleEnum.provider,
        provider_id=2,
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
        email="brainmaskuser@gmail.com",
        key="VCm4-RBXxgtg__yqxf0SYGLHGn8",
        note="BrainMask Key",
    ),
    dict(
        email="prostateimaginguser@gmail.com",
        key="q-jAqPWCRGr2u6SeK6r6U0LBfJA",
        note="ProstateImaging Key",
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
        user_hospital = users[study_data["hospital_user_email"]]
        user_provider = users[study_data["provider_user_email"]]
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
        user = users[study_config_data.pop("provider_user_email")]
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
