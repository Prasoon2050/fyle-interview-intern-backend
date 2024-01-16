import json
import pytest
from flask import Flask, request
from core.apis.decorators import authenticate_principal
from core.libs.exceptions import FyleError

app = Flask(__name__)
app.testing = True

user_data = {
    'user_id': 1,
    'student_id': 101,
    'teacher_id': 201,
    'principal_id': 301
}
principal_header = {'X-Principal': json.dumps(user_data)}

@authenticate_principal
def sample_authenticate_principal(principal):
    return principal

def test_authenticate_principal_invalid_path():
    with app.test_request_context(path='/invalid', headers=principal_header):
        with pytest.raises(FyleError) as excinfo:
            sample_authenticate_principal()
        
        assert 'No such api' in str(excinfo.value.message)
