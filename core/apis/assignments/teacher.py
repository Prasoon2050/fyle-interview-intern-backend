from flask import Blueprint, jsonify, make_response
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    
    teachers_assignments = [assignment for assignment in teachers_assignments if assignment.state != 'DRAFT']
    
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Check if the assignment ID is valid
    assignment = Assignment.get_by_id(grade_assignment_payload['id'])
    if not assignment:
        error_message = 'Assignment not found'
        return make_response(jsonify({'error': 'FyleError', 'message': error_message}), 404)

    # Check if the assignment belongs to the teacher
    if assignment.teacher_id != p.teacher_id:
        error_message = 'You can only grade assignments assigned to you'
        return make_response(jsonify({'error': 'FyleError', 'message': error_message}), 400)

    # Check if the assignment is in the 'SUBMITTED' state
    if assignment.state != 'SUBMITTED':
        error_message = 'Only a submitted assignment can be graded'
        return make_response(jsonify({'error': 'FyleError', 'message': error_message}), 400)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload['id'],
        grade=grade_assignment_payload['grade'],
        auth_principal=p
    )

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
