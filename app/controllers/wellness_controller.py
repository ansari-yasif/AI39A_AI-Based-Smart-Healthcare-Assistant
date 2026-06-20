"""app/controllers/wellness_controller.py — Workout plans (with calorie burn),
health risk predictor, first aid, medicine checker, healthcare finder,
specialist navigator, expense tracker, outbreak alerts, support messages.
"""
from datetime import date, timedelta
from flask import request, redirect, url_for, flash, jsonify
from app.controllers.base_controller import BaseController
from app.models.user import UserModel
from app.models.bmi import BMIModel
from app.models.meal import MealModel
from app.models.medicine import MedicineModel
from app.models.expense import ExpenseModel
from app.models.support import SupportModel
from app.models.outbreak import OutbreakModel
from app.models.notification import NotificationModel
from app.models.workout import WorkoutModel
from app.helpers import today_str, calculate_bmr, calculate_tdee, calculate_bmi


# ════════════════════════════════════════════════════════════════════════
# STATIC CONTENT
# ════════════════════════════════════════════════════════════════════════

# MET values (Metabolic Equivalent of Task) — used to calculate kcal burned
# kcal/min = MET * weight_kg * 0.0175
EXERCISE_MET = {
    'Push-ups': 8.0, 'Bench Press': 6.0, 'Incline Dumbbell Press': 5.0,
    'Chest Dips': 8.0, 'Cable Flyes': 4.0,
    'Pull-ups': 8.0, 'Deadlifts': 6.0, 'Bent-over Rows': 5.0,
    'Lat Pulldown': 4.0, 'Superman Hold': 3.0,
    'Squats': 5.0, 'Lunges': 4.5, 'Romanian Deadlift': 5.0,
    'Leg Press': 4.0, 'Calf Raises': 3.0,
    'Plank': 3.0, 'Crunches': 3.8, 'Russian Twists': 4.0,
    'Leg Raises': 3.8, 'Mountain Climbers': 8.0,
    'Overhead Press': 4.5, 'Lateral Raises': 3.5, 'Bicep Curls': 3.5,
    'Tricep Dips': 4.5, 'Face Pulls': 3.0,
}

WORKOUT_BODY_PARTS = {
    'chest': {
        'name': 'Chest', 'icon': '🫁',
        'exercises': [
            {'name': 'Push-ups', 'sets': '3', 'reps': '12-15', 'duration_min': 8, 'desc': 'Classic bodyweight chest builder. Keep core tight, lower chest to floor.'},
            {'name': 'Bench Press', 'sets': '4', 'reps': '8-10', 'duration_min': 12, 'desc': 'Barbell or dumbbell press lying on a bench. Primary mass builder.'},
            {'name': 'Incline Dumbbell Press', 'sets': '3', 'reps': '10-12', 'duration_min': 10, 'desc': 'Targets upper chest. Set bench to 30-45°.'},
            {'name': 'Chest Dips', 'sets': '3', 'reps': '8-12', 'duration_min': 8, 'desc': 'Lean forward on parallel bars to emphasize chest.'},
            {'name': 'Cable Flyes', 'sets': '3', 'reps': '12-15', 'duration_min': 8, 'desc': 'Isolation move for chest definition and stretch.'},
        ]
    },
    'back': {
        'name': 'Back', 'icon': '🔙',
        'exercises': [
            {'name': 'Pull-ups', 'sets': '3', 'reps': '6-10', 'duration_min': 8, 'desc': 'Best overall back/lat builder using bodyweight.'},
            {'name': 'Deadlifts', 'sets': '4', 'reps': '5-8', 'duration_min': 12, 'desc': 'Full posterior chain — keep back neutral, drive through heels.'},
            {'name': 'Bent-over Rows', 'sets': '3', 'reps': '8-12', 'duration_min': 10, 'desc': 'Barbell or dumbbell row for mid-back thickness.'},
            {'name': 'Lat Pulldown', 'sets': '3', 'reps': '10-12', 'duration_min': 8, 'desc': 'Machine alternative to pull-ups for lats.'},
            {'name': 'Superman Hold', 'sets': '3', 'reps': '30s hold', 'duration_min': 5, 'desc': 'Bodyweight lower-back strengthener — lie face down, lift arms/legs.'},
        ]
    },
    'legs': {
        'name': 'Legs', 'icon': '🦵',
        'exercises': [
            {'name': 'Squats', 'sets': '4', 'reps': '10-12', 'duration_min': 12, 'desc': 'King of leg exercises — quads, glutes, hamstrings.'},
            {'name': 'Lunges', 'sets': '3', 'reps': '12 each leg', 'duration_min': 10, 'desc': 'Unilateral strength and balance for quads/glutes.'},
            {'name': 'Romanian Deadlift', 'sets': '3', 'reps': '10-12', 'duration_min': 10, 'desc': 'Hamstring and glute focused hip-hinge movement.'},
            {'name': 'Leg Press', 'sets': '3', 'reps': '10-15', 'duration_min': 10, 'desc': 'Machine-based quad/glute builder, easier on lower back.'},
            {'name': 'Calf Raises', 'sets': '4', 'reps': '15-20', 'duration_min': 6, 'desc': 'Standing or seated, builds calf strength and definition.'},
        ]
    },
    'core': {
        'name': 'Core / Abs', 'icon': '🎯',
        'exercises': [
            {'name': 'Plank', 'sets': '3', 'reps': '30-60s', 'duration_min': 6, 'desc': 'Isometric core stabilizer — keep hips level, no sagging.'},
            {'name': 'Crunches', 'sets': '3', 'reps': '15-20', 'duration_min': 6, 'desc': 'Classic upper-ab isolation movement.'},
            {'name': 'Russian Twists', 'sets': '3', 'reps': '20 total', 'duration_min': 6, 'desc': 'Rotational core/oblique strengthener.'},
            {'name': 'Leg Raises', 'sets': '3', 'reps': '12-15', 'duration_min': 6, 'desc': 'Lower-ab focused — lie flat, raise legs to 90°.'},
            {'name': 'Mountain Climbers', 'sets': '3', 'reps': '30s', 'duration_min': 6, 'desc': 'Dynamic core + cardio combo movement.'},
        ]
    },
    'shoulders_arms': {
        'name': 'Shoulders & Arms', 'icon': '💪',
        'exercises': [
            {'name': 'Overhead Press', 'sets': '3', 'reps': '8-10', 'duration_min': 10, 'desc': 'Builds shoulder strength and size — press straight up.'},
            {'name': 'Lateral Raises', 'sets': '3', 'reps': '12-15', 'duration_min': 6, 'desc': 'Isolates side delts for shoulder width.'},
            {'name': 'Bicep Curls', 'sets': '3', 'reps': '10-12', 'duration_min': 8, 'desc': 'Dumbbell or barbell curls for bicep size.'},
            {'name': 'Tricep Dips', 'sets': '3', 'reps': '10-12', 'duration_min': 8, 'desc': 'Bodyweight tricep builder using a bench or bars.'},
            {'name': 'Face Pulls', 'sets': '3', 'reps': '15', 'duration_min': 6, 'desc': 'Rear delt and rotator cuff health — great for posture.'},
        ]
    },
}

CARDIO_OPTIONS = [
    {'name': 'Brisk Walking', 'duration_min': 30, 'met': 3.5},
    {'name': 'Jogging', 'duration_min': 25, 'met': 7.0},
    {'name': 'Cycling', 'duration_min': 30, 'met': 6.0},
    {'name': 'Jump Rope', 'duration_min': 12, 'met': 11.0},
    {'name': 'Swimming', 'duration_min': 30, 'met': 7.0},
    {'name': 'HIIT Circuit', 'duration_min': 18, 'met': 9.0},
]

FIRST_AID_GUIDE = [
    {'title': 'Cuts & Scrapes', 'icon': '🩹', 'steps': [
        'Wash your hands before treating the wound.',
        'Rinse the cut under clean running water to remove dirt.',
        'Apply gentle pressure with a clean cloth to stop bleeding.',
        'Apply antiseptic ointment if available.',
        'Cover with a sterile bandage and change daily.',
    ]},
    {'title': 'Burns (Minor)', 'icon': '🔥', 'steps': [
        'Cool the burn under running water for 10-20 minutes.',
        'Do NOT apply ice directly — it can damage skin further.',
        'Remove any tight clothing/jewelry near the burn before swelling starts.',
        'Cover loosely with a sterile, non-fluffy dressing.',
        'Seek medical help if burn is larger than a hand or on face/joints.',
    ]},
    {'title': 'Choking', 'icon': '🫁', 'steps': [
        'Ask "Are you choking?" — if they cannot speak/cough, act fast.',
        'Give 5 back blows between shoulder blades with the heel of your hand.',
        'If unsuccessful, perform 5 abdominal thrusts (Heimlich maneuver).',
        'Alternate back blows and abdominal thrusts until object is dislodged.',
        'Call emergency services if the person becomes unconscious.',
    ]},
    {'title': 'Nosebleed', 'icon': '🩸', 'steps': [
        'Sit down and lean slightly forward (not backward).',
        'Pinch the soft part of the nose firmly for 10-15 minutes.',
        'Breathe through your mouth during this time.',
        'Apply a cold compress to the bridge of the nose.',
        'Seek help if bleeding continues beyond 20 minutes.',
    ]},
    {'title': 'Sprains & Strains', 'icon': '🦴', 'steps': [
        'Follow R.I.C.E: Rest, Ice, Compression, Elevation.',
        'Rest the injured area — avoid putting weight on it.',
        'Apply ice wrapped in cloth for 15-20 minutes every 2-3 hours.',
        'Wrap with an elastic bandage for compression (not too tight).',
        'Elevate the limb above heart level to reduce swelling.',
    ]},
    {'title': 'Fainting', 'icon': '😵', 'steps': [
        'Lay the person flat and raise their legs about 12 inches.',
        'Loosen any tight clothing around neck/waist.',
        'Ensure fresh air — open windows or move away from crowds.',
        'Check breathing; if they don\'t regain consciousness in 1 min, call emergency.',
        'Once awake, let them rest for 10-15 minutes before standing.',
    ]},
    {'title': 'Allergic Reaction', 'icon': '🤧', 'steps': [
        'Remove the allergen if known (food, sting, etc.).',
        'For mild reactions, an antihistamine can help.',
        'Watch for signs of anaphylaxis: difficulty breathing, swelling of face/throat, dizziness.',
        'If severe (anaphylaxis), use an epinephrine auto-injector if available.',
        'Call emergency services immediately for severe reactions.',
    ]},
    {'title': 'Fever Management', 'icon': '🌡️', 'steps': [
        'Rest and stay hydrated with water or oral rehydration solutions.',
        'Dress in lightweight clothing — don\'t overheat or overcool.',
        'Use a lukewarm sponge bath if the fever feels uncomfortable.',
        'Paracetamol/acetaminophen can help reduce fever (follow dosage).',
        'Seek medical care if fever exceeds 39.5°C (103°F) or lasts >3 days.',
    ]},
    {'title': 'Heat Exhaustion', 'icon': '☀️', 'steps': [
        'Move the person to a cool, shaded area immediately.',
        'Remove excess clothing and fan the skin.',
        'Apply cool, wet cloths to neck, armpits, and groin.',
        'Give small sips of water if they are alert and not nauseous.',
        'Seek emergency care if confusion, vomiting, or high body temp occurs (heat stroke).',
    ]},
    {'title': 'Insect Bites & Stings', 'icon': '🐝', 'steps': [
        'Remove the stinger by scraping (don\'t squeeze, it can release more venom).',
        'Wash the area with soap and water.',
        'Apply a cold pack to reduce swelling and pain.',
        'Apply calamine lotion or hydrocortisone cream for itching.',
        'Watch for allergic reaction signs — seek help if breathing is affected.',
    ]},
    {'title': 'Eye Injuries (Foreign Object)', 'icon': '👁️', 'steps': [
        'Do not rub the eye — this can cause more damage.',
        'Try blinking repeatedly to let tears flush the object out.',
        'Rinse gently with clean water or saline solution.',
        'If object is embedded or stuck, do not remove it — cover both eyes lightly.',
        'Seek emergency eye care immediately for embedded objects or chemical exposure.',
    ]},
    {'title': 'Muscle Cramps', 'icon': '🦵', 'steps': [
        'Stop the activity causing the cramp immediately.',
        'Gently stretch and massage the affected muscle.',
        'Apply a warm compress to relax the muscle, or ice if swollen.',
        'Stay hydrated and replenish electrolytes (water with a pinch of salt).',
        'If cramps are frequent, consult a doctor about magnesium/potassium levels.',
    ]},
    {'title': 'Vomiting & Diarrhea', 'icon': '🤢', 'steps': [
        'Stay hydrated with small, frequent sips of water or oral rehydration salts.',
        'Avoid solid food until vomiting subsides — then try bland foods (rice, toast, bananas).',
        'Rest and avoid dairy, caffeine, and fatty foods.',
        'Wash hands frequently to prevent spreading infection.',
        'Seek care if symptoms last more than 2 days or show blood/severe dehydration.',
    ]},
    {'title': 'Headache / Migraine', 'icon': '🤕', 'steps': [
        'Rest in a quiet, dark room.',
        'Apply a cold or warm compress to the forehead/neck.',
        'Stay hydrated — dehydration is a common headache trigger.',
        'Over-the-counter pain relief (paracetamol/ibuprofen) can help if needed.',
        'Seek medical attention for sudden severe "worst ever" headaches or with vision changes.',
    ]},
    {'title': 'Minor Electric Shock', 'icon': '⚡', 'steps': [
        'Turn off the power source before touching the person if possible.',
        'If you cannot turn it off, use a non-conductive object to separate them from the source.',
        'Check for breathing and responsiveness once safe to approach.',
        'Treat any visible burns at contact points as burn injuries.',
        'Seek medical evaluation even for "minor" shocks — internal effects can be delayed.',
    ]},
    {'title': 'Animal Bites', 'icon': '🐕', 'steps': [
        'Wash the wound thoroughly with soap and water for at least 5 minutes.',
        'Apply gentle pressure with a clean cloth to control bleeding.',
        'Apply antiseptic and cover with a sterile bandage.',
        'Note the animal\'s details (owner, vaccination status) if possible.',
        'Seek medical care for rabies/tetanus risk assessment, especially for deep bites.',
    ]},
    {'title': 'Asthma Attack', 'icon': '🫁', 'steps': [
        'Help the person sit upright — do not lie them down.',
        'Help them use their reliever inhaler (usually blue) — 1 puff every 30-60s, up to 10 puffs.',
        'Encourage slow, steady breathing.',
        'Loosen tight clothing around chest and neck.',
        'Call emergency services if no improvement after 10 puffs or lips/fingertips turn blue.',
    ]},
    {'title': 'Sunburn', 'icon': '🏖️', 'steps': [
        'Get out of the sun immediately and cool the skin with a damp cloth.',
        'Take a cool (not cold) shower or bath.',
        'Apply aloe vera gel or moisturizer to soothe skin.',
        'Stay hydrated — drink extra water.',
        'Seek medical care for blistering, fever, or signs of heat illness.',
    ]},
    {'title': 'Splinters', 'icon': '🪵', 'steps': [
        'Wash hands and the area around the splinter.',
        'Use clean tweezers to grasp the splinter at the angle it entered.',
        'Pull out gently in the same direction it went in.',
        'Wash the area again and apply antiseptic.',
        'See a doctor if the splinter is deep, broken off, or the area becomes infected.',
    ]},
    {'title': 'Dehydration', 'icon': '💧', 'steps': [
        'Move to a cool area and rest.',
        'Sip water slowly — avoid gulping large amounts at once.',
        'Use oral rehydration salts (ORS) if available for faster recovery.',
        'Avoid alcohol, caffeine, and sugary drinks.',
        'Seek medical care for severe symptoms: confusion, no urination, rapid heartbeat.',
    ]},
]

SPECIALISTS = [
    {'condition': 'Diabetes / High Blood Sugar', 'specialist': 'Endocrinologist',
     'desc': 'Manages hormonal disorders including diabetes, thyroid issues, and metabolic conditions.'},
    {'condition': 'High BMI / Obesity', 'specialist': 'Nutritionist / Bariatric Specialist',
     'desc': 'Provides diet plans and, if needed, surgical weight-loss options.'},
    {'condition': 'Chest Pain / High Cholesterol', 'specialist': 'Cardiologist',
     'desc': 'Diagnoses and treats heart and blood vessel conditions.'},
    {'condition': 'Joint Pain / Sports Injury', 'specialist': 'Orthopedic Doctor',
     'desc': 'Treats bones, joints, ligaments, and muscle injuries.'},
    {'condition': 'Persistent Cough / Breathing Issues', 'specialist': 'Pulmonologist',
     'desc': 'Specializes in lung and respiratory tract conditions like asthma, COPD.'},
    {'condition': 'Skin Rashes / Acne', 'specialist': 'Dermatologist',
     'desc': 'Diagnoses and treats skin, hair, and nail conditions.'},
    {'condition': 'Anxiety / Depression / Stress', 'specialist': 'Psychiatrist / Psychologist',
     'desc': 'Provides mental health assessment, therapy, and medication management.'},
    {'condition': 'Digestive Issues / Stomach Pain', 'specialist': 'Gastroenterologist',
     'desc': 'Specializes in digestive system disorders (stomach, liver, intestines).'},
    {'condition': 'Frequent Headaches / Migraines', 'specialist': 'Neurologist',
     'desc': 'Diagnoses and treats brain, spine, and nervous system disorders.'},
    {'condition': 'Vision Problems', 'specialist': 'Ophthalmologist',
     'desc': 'Eye care specialist for vision issues and eye diseases.'},
    {'condition': 'Kidney Issues / Frequent UTIs', 'specialist': 'Nephrologist / Urologist',
     'desc': 'Treats kidney function disorders and urinary tract conditions.'},
    {'condition': 'General Checkup / Unclear Symptoms', 'specialist': 'General Physician',
     'desc': 'First point of contact — can refer you to the right specialist.'},
]


class WellnessController(BaseController):

    # ════════════════════════════════════════════════════════════════════
    # WORKOUT PLAN GENERATOR — with daily calorie-burn targets
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def _user_weight(cls, user):
        try:
            w = float(user.get('weight_kg') or 0) if user else 0
            return w if w > 0 else 70.0
        except Exception:
            return 70.0

    @classmethod
    def _kcal_for_exercise(cls, exercise_name, duration_min, weight_kg):
        met = EXERCISE_MET.get(exercise_name, 5.0)
        return round(met * weight_kg * 0.0175 * duration_min)

    @classmethod
    def _kcal_for_cardio(cls, met, duration_min, weight_kg):
        return round(met * weight_kg * 0.0175 * duration_min)

    @classmethod
    def _build_workout_plan_data(cls, uid, user):
        latest_bmi = BMIModel.latest(uid)
        bmi_val = float(latest_bmi['bmi_value']) if latest_bmi else 0
        bmi_label = latest_bmi['bmi_label'] if latest_bmi else 'Unknown'
        goal = (user.get('goal') if user else None) or 'maintain'
        weight_kg = cls._user_weight(user)

        suggestions = cls._get_suggestions(bmi_val, goal)

        # Annotate body part exercises with kcal burn
        body_parts = {}
        daily_burn_total = 0
        for key, part in WORKOUT_BODY_PARTS.items():
            exercises = []
            part_total = 0
            for ex in part['exercises']:
                kcal = cls._kcal_for_exercise(ex['name'], ex['duration_min'], weight_kg)
                part_total += kcal
                exercises.append({**ex, 'kcal': kcal})
            body_parts[key] = {**part, 'exercises': exercises, 'total_kcal': part_total}
            daily_burn_total += part_total

        # Cardio with kcal burn
        cardio = []
        cardio_total = 0
        for c in CARDIO_OPTIONS:
            kcal = cls._kcal_for_cardio(c['met'], c['duration_min'], weight_kg)
            cardio_total += kcal
            cardio.append({**c, 'kcal': kcal})

        # Daily target: based on goal, recommend a kcal-burn target via exercise
        if goal == 'lose':
            daily_target = 400
        elif goal == 'gain':
            daily_target = 200
        else:
            daily_target = 300

        return {
            'bmi_val': bmi_val, 'bmi_label': bmi_label, 'goal': goal,
            'weight_kg': weight_kg, 'suggestions': suggestions,
            'body_parts': body_parts, 'cardio': cardio,
            'daily_burn_total': daily_burn_total, 'cardio_total': cardio_total,
            'daily_target': daily_target,
        }

    @classmethod
    def workout_plan(cls):
        uid  = cls.uid()
        user = UserModel.find_by_id(uid)
        data = cls._build_workout_plan_data(uid, user)
        return cls.render('wellness/workout_plan.html', user=user, today=today_str(), **data)

    @classmethod
    def workout_plan_pdf(cls):
        from flask import make_response
        import io
        uid  = cls.uid()
        user = UserModel.find_by_id(uid)
        data = cls._build_workout_plan_data(uid, user)
        username = (user.get('full_name') or 'User') if user else 'User'

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors as rl_colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
            styles = getSampleStyleSheet()
            TEAL = rl_colors.HexColor('#00C897')
            BLUE = rl_colors.HexColor('#4A9EFF')
            DARK, DARK2 = rl_colors.HexColor('#0f1629'), rl_colors.HexColor('#141e32')
            BORDER = rl_colors.HexColor('#1e2d50')

            title_s = ParagraphStyle('T', parent=styles['Normal'], fontSize=20, textColor=TEAL, fontName='Helvetica-Bold', spaceAfter=4)
            h2_s = ParagraphStyle('H2', parent=styles['Normal'], fontSize=13, textColor=BLUE, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)
            body_s = ParagraphStyle('B', parent=styles['Normal'], fontSize=9, textColor=rl_colors.white, leading=14, spaceAfter=4)

            story = [Paragraph('VitaPulse — Personalised Workout Plan', title_s),
                     Paragraph(f"User: {username} | BMI: {data['bmi_val']} ({data['bmi_label']}) | Goal: {data['goal']} | Weight: {data['weight_kg']}kg | Generated: {today_str()}",
                               ParagraphStyle('sub', parent=styles['Normal'], fontSize=10, textColor=rl_colors.HexColor('#94a3b8'))),
                     HRFlowable(width='100%', thickness=1, color=TEAL, spaceAfter=8)]

            story.append(Paragraph('Recommendations', h2_s))
            for s in data['suggestions']:
                story.append(Paragraph(f'• {s}', body_s))

            story.append(Paragraph(f"Daily Calorie Burn Target: ~{data['daily_target']} kcal", h2_s))
            story.append(Paragraph(
                f"Full body-part routine burns ~{data['daily_burn_total']} kcal · "
                f"Cardio options burn ~{data['cardio_total']} kcal combined.", body_s))

            for key, part in data['body_parts'].items():
                story.append(Paragraph(f"{part['icon']} {part['name']} — ~{part['total_kcal']} kcal", h2_s))
                rows = [['Exercise', 'Sets', 'Reps', 'Time', 'kcal', 'Description']]
                for ex in part['exercises']:
                    rows.append([ex['name'], ex['sets'], ex['reps'], f"{ex['duration_min']}min", str(ex['kcal']), ex['desc']])
                t = Table(rows, colWidths=[3*cm, 1.2*cm, 1.8*cm, 1.3*cm, 1.2*cm, 7.5*cm])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), rl_colors.HexColor('#0a3d2e')),
                    ('TEXTCOLOR', (0,0), (-1,0), TEAL),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0,1), (-1,-1), DARK),
                    ('TEXTCOLOR', (0,1), (-1,-1), rl_colors.white),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [DARK, DARK2]),
                    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
                    ('FONTSIZE', (0,0), (-1,-1), 8),
                    ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ]))
                story.append(t)
                story.append(Spacer(1, 0.3*cm))

            story.append(Paragraph('Cardio Options', h2_s))
            crows = [['Activity', 'Duration', 'Calories Burned']]
            for c in data['cardio']:
                crows.append([c['name'], f"{c['duration_min']} min", f"~{c['kcal']} kcal"])
            ct = Table(crows, colWidths=[6*cm, 4*cm, 4*cm])
            ct.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), rl_colors.HexColor('#0a3d2e')),
                ('TEXTCOLOR', (0,0), (-1,0), TEAL),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BACKGROUND', (0,1), (-1,-1), DARK),
                ('TEXTCOLOR', (0,1), (-1,-1), rl_colors.white),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [DARK, DARK2]),
                ('GRID', (0,0), (-1,-1), 0.4, BORDER),
                ('FONTSIZE', (0,0), (-1,-1), 9),
            ]))
            story.append(ct)

            doc.build(story)
            resp = make_response(buf.getvalue())
            resp.headers['Content-Type'] = 'application/pdf'
            resp.headers['Content-Disposition'] = 'attachment; filename="vitapulse_workout_plan.pdf"'
            return resp
        except ImportError:
            resp = make_response('Workout plan PDF requires reportlab. Run: pip install reportlab')
            resp.headers['Content-Type'] = 'text/plain'
            return resp

    @classmethod
    def _get_suggestions(cls, bmi_val, goal):
        suggestions = []
        if bmi_val == 0:
            suggestions.append('Complete your BMI Calculator first to get a personalised workout plan.')
        elif bmi_val < 18.5:
            suggestions.append('Underweight — focus on strength training 4x/week with progressive overload, plus a calorie surplus diet.')
        elif bmi_val < 25:
            suggestions.append('Healthy BMI — maintain with strength training (3-4x/week) and cardio (2-3x/week).')
        elif bmi_val < 30:
            suggestions.append('Overweight — moderate cardio (4-5x/week, 30 min) + full-body resistance training (3x/week).')
        else:
            suggestions.append('Obese range — start with low-impact cardio 20-30 min daily + bodyweight training 2-3x/week. Consult a doctor first.')
        if goal == 'lose':
            suggestions.append('Goal: Fat Loss — caloric deficit + full-body strength + 150min/week cardio. Aim to burn ~400 kcal/day through exercise.')
        elif goal == 'gain':
            suggestions.append('Goal: Muscle Gain — progressive overload + caloric surplus + 1.6-2.2g/kg protein. Aim for ~200 kcal/day from training (don\'t overdo cardio).')
        else:
            suggestions.append('Goal: Maintenance — balanced training split, aim for ~300 kcal/day burned through activity.')
        return suggestions

    # ════════════════════════════════════════════════════════════════════
    # HEALTH RISK PREDICTOR / EMERGENCY DETECTION
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def health_risk(cls):
        uid  = cls.uid()
        user = UserModel.find_by_id(uid)
        latest_bmi = BMIModel.latest(uid)
        avg_cal = cls._avg_calories_7d(uid)
        from app.helpers import month_range
        ms, me = month_range()
        exp_sum = ExpenseModel.total_for_period(uid, ms, me)

        bmi_val = float(latest_bmi['bmi_value']) if latest_bmi else 0
        risks = cls._compute_risks(user, bmi_val, avg_cal, exp_sum.get('total', 0))

        return cls.render('wellness/health_risk.html',
            user=user, bmi_val=bmi_val, risks=risks,
            avg_cal=avg_cal, today=today_str(),
        )

    @classmethod
    def _avg_calories_7d(cls, uid):
        from app.models.calorie import CalorieModel
        total, days = 0, 0
        for i in range(7):
            d = (date.today() - timedelta(days=i)).isoformat()
            row = CalorieModel.today(uid, d)
            if row:
                total += int(row['calories_consumed'] or 0)
                days += 1
        return round(total / days, 0) if days else 0

    @classmethod
    def _compute_risks(cls, user, bmi_val, avg_cal, month_expense=0):
        """Simple rule-based risk scoring — NOT a medical diagnosis."""
        risks = []
        age = int(user.get('age') or 0) if user else 0
        activity = float(user.get('activity_level') or 1.55) if user else 1.55

        if bmi_val >= 30:
            risks.append({'name': 'Obesity-related conditions', 'level': 'High',
                'color': '#ef4444', 'pct': 75,
                'desc': 'BMI ≥30 increases risk of type 2 diabetes, heart disease, and joint problems. Consult a physician for a personalised plan.'})
        elif bmi_val >= 25:
            risks.append({'name': 'Weight-related risk', 'level': 'Moderate',
                'color': '#f59e0b', 'pct': 45,
                'desc': 'BMI in overweight range — moderate risk for cardiovascular strain. Regular exercise and diet monitoring recommended.'})
        elif bmi_val > 0 and bmi_val < 18.5:
            risks.append({'name': 'Underweight risk', 'level': 'Moderate',
                'color': '#3b82f6', 'pct': 40,
                'desc': 'Being underweight can weaken immune response and bone density. Consider a nutrient-dense diet plan.'})
        else:
            risks.append({'name': 'Weight-related risk', 'level': 'Low',
                'color': '#22c55e', 'pct': 15,
                'desc': 'Your BMI is within the healthy range — keep up consistent habits.'})

        if activity <= 1.2:
            risks.append({'name': 'Sedentary lifestyle', 'level': 'High',
                'color': '#ef4444', 'pct': 70,
                'desc': 'Low activity level increases risk of cardiovascular disease, poor circulation, and metabolic slowdown. Aim for at least 150 min/week of movement.'})
        elif activity <= 1.375:
            risks.append({'name': 'Activity level', 'level': 'Moderate',
                'color': '#f59e0b', 'pct': 40,
                'desc': 'Light activity is a good start — adding 1-2 more active days/week would reduce risk further.'})
        else:
            risks.append({'name': 'Activity level', 'level': 'Low',
                'color': '#22c55e', 'pct': 10,
                'desc': 'Good activity level — keep maintaining regular exercise.'})

        if avg_cal == 0:
            risks.append({'name': 'Nutrition tracking', 'level': 'Unknown',
                'color': '#64748b', 'pct': 50,
                'desc': 'No recent meal logs found — log meals to enable nutrition risk analysis.'})
        elif avg_cal < 1200:
            risks.append({'name': 'Caloric deficiency risk', 'level': 'High',
                'color': '#ef4444', 'pct': 65,
                'desc': f'Average intake of {int(avg_cal)} kcal/day is very low — may indicate malnutrition risk or restrictive eating. Consider consulting a nutritionist.'})
        elif avg_cal > 3000:
            risks.append({'name': 'Excess caloric intake', 'level': 'Moderate',
                'color': '#f59e0b', 'pct': 45,
                'desc': f'Average intake of {int(avg_cal)} kcal/day is on the higher side — monitor portion sizes if weight gain is unwanted.'})
        else:
            risks.append({'name': 'Nutrition balance', 'level': 'Low',
                'color': '#22c55e', 'pct': 15,
                'desc': f'Average intake of {int(avg_cal)} kcal/day looks reasonable for most adults.'})

        if age >= 50:
            risks.append({'name': 'Age-related screening', 'level': 'Moderate',
                'color': '#f59e0b', 'pct': 50,
                'desc': 'At age 50+, regular screenings for blood pressure, cholesterol, and blood sugar are recommended annually.'})
        elif age >= 40:
            risks.append({'name': 'Age-related screening', 'level': 'Low-Moderate',
                'color': '#f59e0b', 'pct': 30,
                'desc': 'At 40+, periodic health checkups help catch early warning signs.'})

        if month_expense > 5000:
            risks.append({'name': 'High medical spending', 'level': 'Moderate',
                'color': '#f97316', 'pct': 55,
                'desc': f'Current monthly health spending ({int(month_expense)}) is significantly high. This may indicate recurring medical needs that require consistent monitoring.'})

        overall_pct = round(sum(r['pct'] for r in risks) / len(risks)) if risks else 0
        if overall_pct >= 60:
            overall = {'level': 'High Risk', 'color': '#ef4444'}
        elif overall_pct >= 35:
            overall = {'level': 'Moderate Risk', 'color': '#f59e0b'}
        else:
            overall = {'level': 'Low Risk', 'color': '#22c55e'}
        overall['pct'] = overall_pct
        return {'risk_list': risks, 'items': risks, 'overall': overall}

    # ════════════════════════════════════════════════════════════════════
    # FIRST AID GUIDE
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def first_aid(cls):
        return cls.render('wellness/first_aid.html', guides=FIRST_AID_GUIDE)

    # ════════════════════════════════════════════════════════════════════
    # SPECIALIST NAVIGATOR
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def specialist_navigator(cls):
        return cls.render('wellness/specialist_navigator.html', specialists=SPECIALISTS)

    # ════════════════════════════════════════════════════════════════════
    # NEARBY HEALTHCARE FINDER
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def healthcare_finder(cls):
        return cls.render('wellness/healthcare_finder.html')

    # ════════════════════════════════════════════════════════════════════
    # MEDICINE CHECKER / REMINDER
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def medicine_index(cls):
        uid = cls.uid()
        meds = MedicineModel.get_for_user(uid)
        today_logs = MedicineModel.today_log(uid, today_str())
        taken_ids = {(l['medicine_id'], l['scheduled_time']) for l in today_logs}
        recent_logs = MedicineModel.recent_logs(uid, 15)
        return cls.render('wellness/medicine_checker.html',
            meds=meds, taken_ids=taken_ids, recent_logs=recent_logs, today=today_str())

    @classmethod
    def medicine_add(cls):
        uid = cls.uid()
        name = request.form.get('name', '').strip()
        dosage = request.form.get('dosage', '').strip()
        times_list = request.form.getlist('times[]') or request.form.getlist('times')
        times = ','.join([t for t in times_list if t])
        frequency = request.form.get('frequency', 'daily')
        start_date = request.form.get('start_date', '') or today_str()
        end_date = request.form.get('end_date', '') or None
        notes = request.form.get('notes', '')

        if not name or not times:
            flash('Medicine name and at least one time are required.', 'danger')
            return redirect(url_for('wellness.medicine_index'))

        MedicineModel.add(uid, name, dosage, times, frequency, start_date, end_date, notes)
        NotificationModel.create(uid, f'Medicine reminder set: {name} 💊',
            f'Scheduled at {times}', 'health', '/wellness/medicine')
        flash(f'{name} reminder added!', 'success')
        return redirect(url_for('wellness.medicine_index'))

    @classmethod
    def medicine_mark_taken(cls):
        uid = cls.uid()
        mid = int(request.form.get('medicine_id'))
        sched_time = request.form.get('time', '')
        MedicineModel.log_dose(mid, uid, today_str(), sched_time, 'taken')
        flash('Marked as taken!', 'success')
        return redirect(url_for('wellness.medicine_index'))

    @classmethod
    def medicine_delete(cls, mid):
        uid = cls.uid()
        MedicineModel.delete(mid, uid)
        flash('Medicine reminder removed.', 'info')
        return redirect(url_for('wellness.medicine_index'))

    @classmethod
    def medicine_due_check(cls):
        """JSON endpoint — returns medicines due now (±5 min window)."""
        from flask import session
        from datetime import datetime
        uid = session.get('user_id')
        if not uid:
            return jsonify({'due': [], 'now': ''})
        now_str = datetime.now().strftime('%H:%M')
        try:
            meds = MedicineModel.get_for_user(uid) or []
        except Exception:
            return jsonify({'due': [], 'now': now_str})
        due = []
        for m in meds:
            for t in (m['times'] or '').split(','):
                t = t.strip()
                if t:
                    diff = cls._time_diff_minutes(now_str, t)
                    if 0 <= diff <= 5:  # due in next 5 min or just past
                        due.append({
                            'id': m['id'],
                            'name': m['name'],
                            'dosage': m.get('dosage') or '',
                            'time': t,
                            'notes': m.get('notes') or ''
                        })
        return jsonify({'due': due, 'now': now_str})

    @staticmethod
    def _time_diff_minutes(now_str, scheduled_str):
        """Returns minutes since scheduled time (positive = overdue)."""
        try:
            h1, m1 = map(int, now_str.split(':'))
            h2, m2 = map(int, scheduled_str.split(':'))
            return (h1*60+m1) - (h2*60+m2)
        except Exception:
            return 9999

    # ════════════════════════════════════════════════════════════════════
    # HEALTH EXPENSE TRACKER
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def expense_index(cls):
        uid = cls.uid()
        from app.helpers import month_range
        try:
            ms, me = month_range()
            month_total = ExpenseModel.total_for_period(uid, ms, me) or {'total': 0, 'cnt': 0}
            by_cat      = ExpenseModel.by_category(uid, ms, me) or []
            trend       = ExpenseModel.monthly_trend(uid, 6) or []
            recent      = ExpenseModel.get_for_user(uid, 50) or []
        except Exception as e:
            month_total = {'total': 0, 'cnt': 0}
            by_cat = trend = recent = []
        CATEGORIES = ['Medicine', 'Doctor Visit', 'Lab Test', 'Hospital', 'Insurance', 'Supplements', 'Other']
        return cls.render('wellness/expense_tracker.html',
            month_total=month_total, by_cat=by_cat, trend=trend,
            recent=recent, categories=CATEGORIES, today=today_str())

    @classmethod
    def expense_add(cls):
        uid = cls.uid()
        category = request.form.get('category', 'Other')
        description = request.form.get('description', '')
        expense_date = request.form.get('expense_date', today_str())
        try:
            amount = float(request.form.get('amount', 0))
            if amount <= 0:
                raise ValueError
            res = ExpenseModel.add(uid, category, amount, description, expense_date)
            if res:
                NotificationModel.create(uid, f'Expense logged: {amount} 💸',
                    f'{category}: {description[:30]}...', 'health', '/wellness/expenses')
                flash(f'Expense of {amount} logged under {category}.', 'success')
            else:
                flash('Failed to log expense. Database table might be missing.', 'danger')
        except ValueError:
            flash('Please enter a valid amount.', 'danger')
        return redirect(url_for('wellness.expense_index'))

    @classmethod
    def expense_delete(cls, eid):
        uid = cls.uid()
        ExpenseModel.delete(eid, uid)
        flash('Expense removed.', 'info')
        return redirect(url_for('wellness.expense_index'))

    @classmethod
    def expense_pdf(cls):
        from flask import make_response
        import io
        uid = cls.uid()
        user = UserModel.find_by_id(uid)
        from app.helpers import month_range
        ms, me = month_range()
        recent = ExpenseModel.get_for_user(uid, 200)
        by_cat = ExpenseModel.by_category(uid, ms, me)
        month_total = ExpenseModel.total_for_period(uid, ms, me)
        username = (user.get('full_name') or 'User') if user else 'User'

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors as rl_colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
            styles = getSampleStyleSheet()
            TEAL = rl_colors.HexColor('#00C897')
            BLUE = rl_colors.HexColor('#4A9EFF')
            DARK, DARK2 = rl_colors.HexColor('#0f1629'), rl_colors.HexColor('#141e32')
            BORDER = rl_colors.HexColor('#1e2d50')

            title_s = ParagraphStyle('T', parent=styles['Normal'], fontSize=20, textColor=TEAL, fontName='Helvetica-Bold', spaceAfter=4)
            h2_s = ParagraphStyle('H2', parent=styles['Normal'], fontSize=13, textColor=BLUE, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)

            story = [Paragraph('VitaPulse — Health Expense Report', title_s),
                     Paragraph(f'User: {username} | Month Total: {month_total["total"]} | Generated: {today_str()}',
                               ParagraphStyle('sub', parent=styles['Normal'], fontSize=10, textColor=rl_colors.HexColor('#94a3b8'))),
                     HRFlowable(width='100%', thickness=1, color=TEAL, spaceAfter=8)]

            story.append(Paragraph('By Category (This Month)', h2_s))
            crows = [['Category', 'Total', 'Count']]
            for c in by_cat:
                crows.append([c['category'], str(c['total']), str(c['cnt'])])
            ct = Table(crows, colWidths=[6*cm, 4*cm, 4*cm])
            ct.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), rl_colors.HexColor('#0a3d2e')),
                ('TEXTCOLOR', (0,0), (-1,0), TEAL),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BACKGROUND', (0,1), (-1,-1), DARK),
                ('TEXTCOLOR', (0,1), (-1,-1), rl_colors.white),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [DARK, DARK2]),
                ('GRID', (0,0), (-1,-1), 0.4, BORDER),
                ('FONTSIZE', (0,0), (-1,-1), 9),
            ]))
            story.append(ct)
            story.append(Spacer(1, 0.4*cm))

            story.append(Paragraph('Recent Transactions', h2_s))
            rows = [['Date', 'Category', 'Amount', 'Description']]
            for r in recent:
                rows.append([str(r['expense_date']), r['category'], str(r['amount']), (r['description'] or '')[:40]])
            t = Table(rows, colWidths=[3*cm, 3.5*cm, 2.5*cm, 7*cm])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), rl_colors.HexColor('#0a3d2e')),
                ('TEXTCOLOR', (0,0), (-1,0), TEAL),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BACKGROUND', (0,1), (-1,-1), DARK),
                ('TEXTCOLOR', (0,1), (-1,-1), rl_colors.white),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [DARK, DARK2]),
                ('GRID', (0,0), (-1,-1), 0.4, BORDER),
                ('FONTSIZE', (0,0), (-1,-1), 8),
            ]))
            story.append(t)

            doc.build(story)
            resp = make_response(buf.getvalue())
            resp.headers['Content-Type'] = 'application/pdf'
            resp.headers['Content-Disposition'] = 'attachment; filename="vitapulse_expense_report.pdf"'
            return resp
        except ImportError:
            resp = make_response('PDF requires reportlab.')
            resp.headers['Content-Type'] = 'text/plain'
            return resp

    # ════════════════════════════════════════════════════════════════════
    # SUPPORT / CONTACT ADMIN
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def support_index(cls):
        uid = cls.uid()
        try:
            msgs = SupportModel.get_for_user(uid) or []
        except Exception:
            msgs = []
        return cls.render('wellness/support.html', support_messages=msgs)

    @classmethod
    def support_send(cls):
        uid = cls.uid()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        if not subject or not message:
            flash('Subject and message are required.', 'danger')
            return redirect(url_for('wellness.support_index'))
        try:
            result = SupportModel.create(uid, subject, message)
            if result is None:
                flash('Could not send message — database table may need migration. Run migration_full.sql.', 'danger')
            else:
                # Create notification for admin users
                try:
                    from app.models.user import UserModel
                    from app.models.notification import NotificationModel
                    admins = UserModel.get_admins()
                    for admin in (admins or []):
                        NotificationModel.create(admin['id'], f'New support message from user #{uid}',
                            subject[:100], 'info', '/admin/messages')
                except Exception:
                    pass  # notifications optional
                flash('Message sent to admin! We will reply soon.', 'success')
        except Exception as e:
            flash(f'Error sending message: {str(e)[:80]}', 'danger')
        return redirect(url_for('wellness.support_index'))

    # ════════════════════════════════════════════════════════════════════
    # OUTBREAK ALERTS (read-only for users)
    # ════════════════════════════════════════════════════════════════════
    @classmethod
    def outbreak_banner_data(cls):
        return OutbreakModel.active_alerts()
