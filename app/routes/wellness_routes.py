@wellness_bp.route('/healthcare-finder')
@login_required
def healthcare_finder():
    return WellnessController.healthcare_finder()
