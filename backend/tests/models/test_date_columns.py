def test_user_date_fields(random_test_user, db):
    assert (
        random_test_user.created_at is not None
    ), "Expected created_at column to be automatically added to model"

    assert (
        random_test_user.updated_at is None
    ), "Expected updated_at column to be empty before any updates"

    prev_created_at = random_test_user.created_at
    prev_first_name = random_test_user.first_name

    random_test_user.first_name = prev_first_name + "!"

    db.add(random_test_user)
    db.commit()
    db.refresh(random_test_user)

    assert (
        random_test_user.first_name == prev_first_name + "!"
    ), "Expected first_name to be updated"
    assert (
        random_test_user.updated_at is not None
    ), "Expected updated_at to be populated after update"
    assert (
        random_test_user.updated_at > random_test_user.created_at
    ), "Expected updated_at to be after created_at"
    assert (
        prev_created_at == random_test_user.created_at
    ), "Expected created_at to remain unchanged"
