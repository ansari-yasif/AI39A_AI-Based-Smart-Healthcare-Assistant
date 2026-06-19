def calculate_water_intake(weight_kg: float) -> float:
    """
    Calculate recommended daily water intake in liters.
    Formula: 35ml per kg body weight.
    """
    if weight_kg <= 0:
        return 0.0

    return round((weight_kg * 35) / 1000, 1)