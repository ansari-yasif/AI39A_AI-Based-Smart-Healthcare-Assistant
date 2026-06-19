@wellness_bp.route('/healthcare-finder')
@login_required
def healthcare_finder():
    return WellnessController.healthcare_finder()

@wellness_bp.route('/workout-plan')
@login_required
def workout_plan():
    return WellnessController.workout_plan()

@wellness_bp.route('/workout-plan/pdf')
@login_required
def workout_plan_pdf():
    return WellnessController.workout_plan_pdf()
