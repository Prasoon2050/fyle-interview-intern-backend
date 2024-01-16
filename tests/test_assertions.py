import pytest
from core.libs.exceptions import FyleError
from core.libs.assertions import base_assert, assert_auth, assert_true, assert_valid, assert_found

def test_base_assert_raises_fyle_error():
    with pytest.raises(FyleError) as excinfo:
        base_assert(500, "Internal Server Error")
    assert excinfo.value.status_code == 500
    assert excinfo.value.message == "Internal Server Error"

def test_assert_auth_raises_error_when_false():
    with pytest.raises(FyleError) as excinfo:
        assert_auth(False)
    assert excinfo.value.status_code == 401
    assert excinfo.value.message == "UNAUTHORIZED"

def test_assert_conditions_raise_fyle_error():
    with pytest.raises(FyleError) as excinfo:
        assert_true(False)
    assert excinfo.value.status_code == 403
    assert excinfo.value.message == "FORBIDDEN"

    with pytest.raises(FyleError) as excinfo:
        assert_valid(False)
    assert excinfo.value.status_code == 400
    assert excinfo.value.message == "BAD_REQUEST"

def test_assert_found_raises_error_with_none():
    with pytest.raises(FyleError) as excinfo:
        assert_found(None)
    assert excinfo.value.status_code == 404
    assert excinfo.value.message == "NOT_FOUND"


