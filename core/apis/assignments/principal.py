from flask import Blueprint, jsonify, make_response
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher

from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of all submitted and graded assignments"""
    assignments = Assignment.filter(
        (Assignment.state == AssignmentStateEnum.SUBMITTED) |
        (Assignment.state == AssignmentStateEnum.GRADED)
    ).all()

    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment = Assignment.get_by_id(grade_assignment_payload['id'])
    print(assignment.teacher_id)
    if assignment.state == AssignmentStateEnum.DRAFT:
        error_message = 'Cannot grade assignments in Draft state'
        return make_response(jsonify({'error': 'BadRequest', 'message': error_message}), 400)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload['id'],
        grade=grade_assignment_payload['grade'],
        auth_principal=p
    )
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """List all teachers"""
    teachers = Teacher.query.all()
    teachers_dump = TeacherSchema(many=True).dump(teachers)
    return APIResponse.respond(data=teachers_dump)