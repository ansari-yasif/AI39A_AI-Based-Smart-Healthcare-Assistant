"""app/constants.py — App-wide constants (no magic values in code)"""

MOOD_OPTIONS     = ['Happy', 'Energetic', 'Calm', 'Tired', 'Stressed', 'Sad', 'Anxious', 'Focused']
SLEEP_QUALITY    = ['Excellent', 'Good', 'Fair', 'Poor', 'Very Poor']
MEAL_TYPES       = ['Breakfast', 'Lunch', 'Dinner', 'Snack', 'Pre-Workout', 'Post-Workout']
EXPENSE_CATS     = ['Food & Groceries','Gym & Fitness','Healthcare','Supplements','Equipment','Mental Wellness','Other']
ACTIVITY_LEVELS  = [(1.2,'Sedentary'),(1.375,'Lightly Active'),(1.55,'Moderately Active'),(1.725,'Very Active'),(1.9,'Extra Active')]
BMI_RANGES       = [(0,18.5,'Underweight','#4A9EFF'),(18.5,25,'Normal','#00C897'),(25,30,'Overweight','#F59E0B'),(30,999,'Obese','#EF4444')]
ROLE_USER  = 'user'
ROLE_ADMIN = 'admin'