import src.auth as auth


def use_temp_user_store(monkeypatch, tmp_path):
    users_file = tmp_path / "users.csv"
    monkeypatch.setattr(auth, "USERS_FILE", users_file)
    monkeypatch.setattr(auth, "DATA_DIR", tmp_path)
    return users_file


def test_register_user_hashes_password(monkeypatch, tmp_path):
    users_file = use_temp_user_store(monkeypatch, tmp_path)

    success, message = auth.register_user("new_user", "longpassword", role="user")

    assert success is True
    assert "Registration successful" in message
    contents = users_file.read_text(encoding="utf-8")
    assert "new_user" in contents
    assert "longpassword" not in contents


def test_duplicate_username_is_rejected(monkeypatch, tmp_path):
    use_temp_user_store(monkeypatch, tmp_path)

    auth.register_user("new_user", "longpassword", role="user")
    success, message = auth.register_user("new_user", "anotherlongpassword", role="user")

    assert success is False
    assert message == "This username is already being used. Please choose another username."


def test_authenticate_user_distinguishes_wrong_password(monkeypatch, tmp_path):
    use_temp_user_store(monkeypatch, tmp_path)
    auth.register_user("new_user", "longpassword", role="user")

    assert auth.user_exists("new_user") is True
    assert auth.authenticate_user("new_user", "wrongpassword") is None
    assert auth.authenticate_user("new_user", "longpassword")["role"] == "user"
