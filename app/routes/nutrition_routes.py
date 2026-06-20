@nutrition_bp.route('/macro-targets')
@login_required
def macro_targets_index():
    return NutritionController.macro_targets_index()

@nutrition_bp.route('/macro-targets/save', methods=['POST'])
@login_required
def macro_targets_save():
    return NutritionController.macro_targets_save()
