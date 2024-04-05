from app.schemas import HospitalCreate
from app.services.hospitals import create_hospital
from app.schemas import UserHospitalCreate
from app.services.users import create_hospital_user
from app.schemas.user import UserRoleEnum
from app.services.hospitals import get_hospital_users


def test_hospital_creation(db):
    db_hospital = create_hospital(
        db,
        HospitalCreate.parse_obj(
            {
                "hospital_name": "test_hospital",
            }
        ),
    )

    assert db_hospital.hospital_name == "test_hospital"
    assert db_hospital.created_at is not None


def test_hospital_get_users(db):
    db_hospital_1 = create_hospital(
        db,
        HospitalCreate.parse_obj(
            {
                "hospital_name": "test_hospital_1",
            }
        ),
    )

    db_hospital_2 = create_hospital(
        db,
        HospitalCreate.parse_obj(
            {
                "hospital_name": "test_hospital_2",
            }
        ),
    )

    db_user_1 = create_hospital_user(
        db,
        UserHospitalCreate.parse_obj(
            {
                "email": "bing_bong@example.com",
                "password": "abc",
                "first_name": "Bing",
                "last_name": "Bong",
                "role": UserRoleEnum.hospital,
                "hospital_id": db_hospital_1.id,
            }
        ),
    )

    db_user_2 = create_hospital_user(
        db,
        UserHospitalCreate.parse_obj(
            {
                "email": "jrice@example.com",
                "password": "abc",
                "first_name": "Jerry",
                "last_name": "Rice",
                "role": UserRoleEnum.hospital,
                "hospital_id": db_hospital_2.id,
            }
        ),
    )

    db_user_3 = create_hospital_user(
        db,
        UserHospitalCreate.parse_obj(
            {
                "email": "ikant@example.com",
                "password": "abc",
                "first_name": "Immanuel",
                "last_name": "Kant",
                "role": UserRoleEnum.hospital,
                "hospital_id": db_hospital_1.id,
            }
        ),
    )

    hospital_1_users = get_hospital_users(db, db_hospital_1.id)
    assert len(hospital_1_users) == 2
    assert hospital_1_users[0].first_name == db_user_1.first_name
    assert hospital_1_users[1].first_name == db_user_3.first_name

    hospital_2_users = get_hospital_users(db, db_hospital_2.id)
    assert len(hospital_2_users) == 1
    assert hospital_2_users[0].first_name == db_user_2.first_name
