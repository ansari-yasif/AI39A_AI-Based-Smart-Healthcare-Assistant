@nutrition_bp.route('/macro-targets')
@login_required
def macro_targets_index():
    return NutritionController.macro_targets_index()

@nutrition_bp.route('/macro-targets/save', methods=['POST'])
@login_required
def macro_targets_save():
    return NutritionController.macro_targets_save()
@nutrition_bp.route('/calories')
@login_required
def calorie_index():
    return NutritionController.calorie_index()

@nutrition_bp.route('/calories/goal', methods=['POST'])
@login_required
def update_goal():
    return NutritionController.update_goal()
