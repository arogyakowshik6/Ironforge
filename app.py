import os; os.environ['FLASK_ENV'] = 'development'  # Enable debug mode for development
from flask import Flask, render_template, request, redirect, url_for, session  # type: ignore[import]


app = Flask(__name__)
app.secret_key = 'ironforge-secret-2026'

# ─── Plan Data ────────────────────────────────────────────────────────────────

PLANS = {
    "weight_loss": {
        "name": "Weight Loss / Fat Burn",
        "icon": "🔥",
        "description": "Metabolic conditioning, circuit training and steady-state cardio to maximise calorie burn while preserving lean muscle.",
        "style": "Cardio & Circuits",
        "diet_type": "400–600 kcal deficit",
        "macros": {
            "female": {"kcal": 1500, "protein": 130, "carbs": 130, "fats": 50, "weight": "~70kg"},
            "male":   {"kcal": 1900, "protein": 170, "carbs": 160, "fats": 60, "weight": "~85kg"},
        },
        "macro_rule": "2g protein per kg bodyweight. Calories 400–600 below your TDEE.",
        "days": [
            {
                "day": "Monday", "label": "Full Body Circuit + Cardio", "type": "training",
                "exercises": [
                    {"name": "Jumping Jacks",         "sets": "3 sets × 45 sec", "rest": "15 sec rest",  "tip": "Stand upright, jump feet apart and raise arms overhead. Keep core braced throughout."},
                    {"name": "Bodyweight Squats",     "sets": "4 sets × 15 reps","rest": "45 sec rest",  "tip": "Feet shoulder-width, toes slightly out. Lower hips until thighs are parallel to floor."},
                    {"name": "Push-Ups",              "sets": "3 sets × 12 reps","rest": "45 sec rest",  "tip": "Hands shoulder-width, body straight. Lower chest to floor. Keep elbows at 45 degrees."},
                    {"name": "Mountain Climbers",     "sets": "3 sets × 30 sec", "rest": "20 sec rest",  "tip": "Plank position. Drive alternating knees to chest rapidly. Keep hips level."},
                    {"name": "Dumbbell Row",          "sets": "3 sets × 12/side","rest": "45 sec rest",  "tip": "Lean forward, one hand on bench. Pull dumbbell to hip, elbow driving back."},
                    {"name": "Burpees",               "sets": "3 sets × 10 reps","rest": "60 sec rest",  "tip": "Squat down, jump to plank, push-up, jump in, explode upward with arms raised."},
                    {"name": "Plank Hold",            "sets": "3 sets × 45 sec", "rest": "30 sec rest",  "tip": "Forearms on floor, body straight. Squeeze glutes and core. Breathe steadily."},
                    {"name": "Treadmill Jog",         "sets": "1 × 20 min",      "rest": "",             "tip": "Moderate effort (5–6/10). Incline 1–2%. Focus on steady breathing."},
                ]
            },
            {
                "day": "Tuesday", "label": "Lower Body + Core", "type": "training",
                "exercises": [
                    {"name": "Walking Lunges",        "sets": "4 sets × 12/leg", "rest": "45 sec rest",  "tip": "Step forward and lower back knee toward floor. Push off front foot."},
                    {"name": "Sumo Squats",           "sets": "3 sets × 15 reps","rest": "45 sec rest",  "tip": "Wide stance, toes out 45°. Lower hips, chest up. Squeeze glutes at top."},
                    {"name": "Glute Bridges",         "sets": "4 sets × 20 reps","rest": "30 sec rest",  "tip": "Lie on back, knees bent. Drive hips to ceiling, squeeze glutes hard. Lower slowly."},
                    {"name": "Step-Ups",              "sets": "3 sets × 15/leg", "rest": "45 sec rest",  "tip": "Drive through heel of working leg. Don't push off the trailing foot."},
                    {"name": "Leg Raises",            "sets": "3 sets × 15 reps","rest": "30 sec rest",  "tip": "Lie flat, hands under hips. Raise legs to 90° and lower slowly."},
                    {"name": "Russian Twists",        "sets": "3 sets × 20 reps","rest": "30 sec rest",  "tip": "Sit at 45°, feet off floor. Rotate torso fully side to side."},
                    {"name": "Bicycle Crunches",      "sets": "3 sets × 30 reps","rest": "30 sec rest",  "tip": "Alternate bringing elbow to opposite knee. Do not pull neck."},
                    {"name": "Jump Rope / Skipping",  "sets": "1 × 15 min",      "rest": "",             "tip": "Light rhythmic bounce. Land softly on balls of feet."},
                ]
            },
            {
                "day": "Wednesday", "label": "Active Recovery", "type": "rest",
                "exercises": [],
                "note": "No resistance training. 30-min walk, foam rolling, yoga or light swimming. Drink 3 litres of water. Stretch tight areas from the first two days."
            },
            {
                "day": "Thursday", "label": "Upper Body + HIIT", "type": "training",
                "exercises": [
                    {"name": "Dumbbell Shoulder Press",    "sets": "3 sets × 12 reps","rest": "45 sec rest","tip": "Press from ear height to above head. Don't arch lower back."},
                    {"name": "Dumbbell Bicep Curls",       "sets": "3 sets × 12 reps","rest": "45 sec rest","tip": "Curl both dumbbells, squeeze biceps. Lower slowly over 3 seconds."},
                    {"name": "Tricep Dips",                "sets": "3 sets × 12 reps","rest": "45 sec rest","tip": "Hands on chair edge. Lower to 90°, press back up. Keep back close."},
                    {"name": "Bent-Over Dumbbell Rows",    "sets": "3 sets × 12 reps","rest": "45 sec rest","tip": "Hinge 45°, back flat. Pull to ribcage, elbows close. Squeeze at top."},
                    {"name": "High Knees",                 "sets": "4 sets × 30 sec", "rest": "15 sec rest","tip": "Drive knees above hip height. Stay on balls of feet. Maximum effort."},
                    {"name": "Jump Squats",                "sets": "3 sets × 10 reps","rest": "60 sec rest","tip": "Land softly with bent knees, absorb impact. Reset before next rep."},
                    {"name": "Push-Up to Shoulder Tap",   "sets": "3 sets × 10 reps","rest": "45 sec rest","tip": "At the top, tap each shoulder. Keep hips square. Core tight."},
                    {"name": "Rowing Machine or Bike",     "sets": "1 × 20 min",      "rest": "",           "tip": "Aim for 70% max heart rate. Focus on breathing rhythm."},
                ]
            },
            {
                "day": "Friday", "label": "Full Body HIIT", "type": "training",
                "exercises": [
                    {"name": "Squat to Press",      "sets": "4 sets × 12 reps","rest": "45 sec rest","tip": "Hold dumbbells at shoulders. Squat, stand and press overhead in one fluid motion."},
                    {"name": "Renegade Rows",       "sets": "3 sets × 10/side","rest": "60 sec rest","tip": "Plank with dumbbells. Row one to hip, return, repeat other side. Keep hips still."},
                    {"name": "Lateral Lunges",      "sets": "3 sets × 12/side","rest": "45 sec rest","tip": "Step wide, bend that knee, keep other leg straight. Push back to centre."},
                    {"name": "Flutter Kicks",       "sets": "3 sets × 30 sec", "rest": "30 sec rest","tip": "Legs raised 15cm. Alternate small kicks. Keep lower back pressed to floor."},
                    {"name": "Dumbbell Deadlift",   "sets": "3 sets × 12 reps","rest": "60 sec rest","tip": "Hinge at hips, back flat. Drive hips forward to stand."},
                    {"name": "Speed Skaters",       "sets": "3 sets × 30 sec", "rest": "20 sec rest","tip": "Leap laterally landing on one foot. Mimic an ice skater. Stay light on feet."},
                    {"name": "Stair Climb / Incline Walk","sets": "1 × 20 min","rest": "",           "tip": "High incline (12–15%). Swing arms naturally. Maintain steady pace."},
                ]
            },
            {
                "day": "Saturday", "label": "Cardio & Core Endurance", "type": "training",
                "exercises": [
                    {"name": "Long Walk or Light Jog","sets": "1 × 40 min",      "rest": "",           "tip": "Steady low-intensity. Heart rate 60–65% max. Ideal outdoors."},
                    {"name": "Dead Bug",              "sets": "3 sets × 10/side","rest": "30 sec rest","tip": "Lower opposite arm and leg simultaneously. Keep back flat on floor."},
                    {"name": "Side Plank",            "sets": "3 sets × 30 sec each side","rest": "30 sec rest","tip": "Body in straight line, one forearm on floor. Don't let hips drop."},
                    {"name": "V-Sit Hold",            "sets": "3 sets × 20 sec", "rest": "30 sec rest","tip": "Lean back 45°, raise legs to form a V. Bend knees slightly if needed."},
                    {"name": "Slow Bicycle Crunches", "sets": "3 sets × 20 reps","rest": "30 sec rest","tip": "3-second tempo. Full extension of leg and full rotation each rep."},
                    {"name": "Foam Roll & Stretch",   "sets": "1 × 15 min",      "rest": "",           "tip": "Roll quads, hamstrings, calves, IT band. Hold each stretch 30–45 seconds."},
                ]
            },
            {
                "day": "Sunday", "label": "Full Rest", "type": "rest",
                "exercises": [],
                "note": "Complete rest. No training. Hydrate well, sleep 7–9 hours. Prepare meals for the week ahead."
            },
        ],
        "meals": [
            {"time": "Breakfast",          "meal": "Oats with berries & protein powder",        "detail": "80g oats, 1 scoop protein powder, 100g mixed berries. Slow-release energy, high fibre, antioxidants."},
            {"time": "Mid-Morning Snack",  "meal": "Greek yogurt & almonds",                    "detail": "170g 0% Greek yogurt, 20g almonds. High protein, healthy fats, keeps hunger away."},
            {"time": "Lunch",              "meal": "Grilled chicken with quinoa & salad",       "detail": "180g chicken breast, 80g quinoa, mixed leaves. Lean protein, complete amino acids."},
            {"time": "Afternoon Snack",    "meal": "Apple with peanut butter",                  "detail": "1 medium apple, 1 tbsp peanut butter. Natural sugar and healthy fat."},
            {"time": "Dinner",             "meal": "Baked salmon with sweet potato & broccoli", "detail": "180g salmon, 150g sweet potato, 200g broccoli. Omega-3, slow carbs, vitamins."},
            {"time": "Evening",            "meal": "Cottage cheese",                             "detail": "150g low-fat cottage cheese. Casein protein feeds muscles overnight."},
        ],
        "avoid": ["Sugary drinks (fizzy drinks, fruit juice, sports drinks)", "Processed snacks (crisps, biscuits, chocolate bars, white bread)", "Fried foods (chips, fried chicken, battered fish)", "Alcohol — impairs recovery and fat burning", "High-sugar cereals"],
        "snacks": ["Rice cakes with avocado", "Hard-boiled eggs (2)", "Cucumber slices with hummus", "Protein shake with water (post-workout)", "Mixed berries: blueberries, raspberries, strawberries"],
    },

    "bulking": {
        "name": "Bulking — Muscle Gain",
        "icon": "💪",
        "description": "Progressive overload with heavy compound movements to stimulate maximum muscle growth. Paired with a calorie surplus.",
        "style": "Heavy Compound Lifts",
        "diet_type": "300–500 kcal surplus",
        "macros": {
            "female": {"kcal": 2200, "protein": 140, "carbs": 260, "fats": 65, "weight": "~60kg"},
            "male":   {"kcal": 2900, "protein": 190, "carbs": 340, "fats": 80, "weight": "~80kg"},
        },
        "macro_rule": "Eat 300–500 calories above your TDEE. 2–2.5g protein per kg bodyweight.",
        "days": [
            {
                "day": "Monday", "label": "Chest & Triceps", "type": "training",
                "exercises": [
                    {"name": "Barbell Bench Press",   "sets": "4 sets × 6–8 reps","rest": "90 sec rest","tip": "Lower to lower chest, press explosively up. Keep feet flat, arch natural."},
                    {"name": "Incline Dumbbell Press","sets": "3 sets × 8–10 reps","rest": "75 sec rest","tip": "Bench at 30–45°. Press from chest level up. Feel the upper chest stretch at bottom."},
                    {"name": "Cable Flyes",           "sets": "3 sets × 12 reps", "rest": "60 sec rest","tip": "Arms wide, slight elbow bend. Bring hands together in arc. Squeeze pecs hard at top."},
                    {"name": "Dips",                  "sets": "3 sets × 10 reps", "rest": "60 sec rest","tip": "Lean forward slightly. Lower until shoulders below elbows. Press back up."},
                    {"name": "Skull Crushers",        "sets": "3 sets × 10 reps", "rest": "60 sec rest","tip": "EZ bar above forehead. Bend elbows lowering bar near forehead. Control the lowering."},
                    {"name": "Tricep Pushdowns",      "sets": "3 sets × 12 reps", "rest": "45 sec rest","tip": "Press bar down until arms fully extended. Keep elbows fixed at sides."},
                    {"name": "Push-Up Burnout",       "sets": "1 set to failure", "rest": "",           "tip": "Standard push-ups until form breaks. Finishing set only."},
                ]
            },
            {
                "day": "Tuesday", "label": "Back & Biceps", "type": "training",
                "exercises": [
                    {"name": "Barbell Deadlift",         "sets": "4 sets × 5 reps", "rest": "120 sec rest","tip": "Bar over mid-foot. Push the floor away rather than pulling. Lock hips and shoulders."},
                    {"name": "Pull-Ups / Lat Pulldown",  "sets": "4 sets × 8 reps", "rest": "90 sec rest", "tip": "Full hang, pull elbows to sides, chest to bar. Use lat pulldown if pull-ups not possible."},
                    {"name": "Seated Cable Rows",        "sets": "3 sets × 10 reps","rest": "60 sec rest", "tip": "Sit upright, pull to lower ribs. Squeeze shoulder blades. Don't rock backward."},
                    {"name": "Single-Arm Dumbbell Row",  "sets": "3 sets × 10/side","rest": "60 sec rest", "tip": "Support on bench. Pull to hip, elbow drives back. Full stretch at bottom."},
                    {"name": "Face Pulls",               "sets": "3 sets × 15 reps","rest": "45 sec rest", "tip": "Cable at forehead height. Pull to face, elbows high. Great for posture."},
                    {"name": "Barbell Bicep Curl",       "sets": "3 sets × 10 reps","rest": "60 sec rest", "tip": "Shoulder-width grip. Squeeze hard. Lower over 3 seconds. No swinging."},
                    {"name": "Hammer Curls",             "sets": "3 sets × 12 reps","rest": "45 sec rest", "tip": "Palms facing each other. Curl alternately. Slow negative for max growth stimulus."},
                ]
            },
            {
                "day": "Wednesday", "label": "Legs & Glutes", "type": "training",
                "exercises": [
                    {"name": "Barbell Back Squat",  "sets": "4 sets × 6–8 reps","rest": "120 sec rest","tip": "Bar on traps, feet shoulder-width. Sit back and down. Drive through heels to lockout."},
                    {"name": "Romanian Deadlift",   "sets": "3 sets × 10 reps", "rest": "90 sec rest", "tip": "Hinge at hips, slight knee bend. Feel the hamstring stretch, drive hips forward."},
                    {"name": "Leg Press",           "sets": "4 sets × 12 reps", "rest": "75 sec rest", "tip": "Push through heels. Don't lock knees at top. Full range of motion every rep."},
                    {"name": "Walking Lunges",      "sets": "3 sets × 12/leg",  "rest": "60 sec rest", "tip": "Hold dumbbells. Large step forward, lower back knee near floor. Alternate."},
                    {"name": "Leg Curl Machine",    "sets": "3 sets × 12 reps", "rest": "60 sec rest", "tip": "Curl heels toward glutes. Squeeze hamstrings hard. Lower slowly."},
                    {"name": "Calf Raises",         "sets": "4 sets × 20 reps", "rest": "45 sec rest", "tip": "On step edge. Full range. Hold 1 second at top. Use heavy weight if possible."},
                    {"name": "Hip Thrust",          "sets": "3 sets × 15 reps", "rest": "60 sec rest", "tip": "Upper back on bench, bar across hips. Drive hips to ceiling. Squeeze at top for 1 second."},
                ]
            },
            {
                "day": "Thursday", "label": "Rest / Active Recovery", "type": "rest",
                "exercises": [],
                "note": "Light activity only. 30-min walk, foam rolling, or yoga. Essential for muscle repair and growth. Drink plenty of water."
            },
            {
                "day": "Friday", "label": "Shoulders & Traps", "type": "training",
                "exercises": [
                    {"name": "Barbell Overhead Press","sets": "4 sets × 6–8 reps","rest": "90 sec rest","tip": "Press from collar bones to above head. Lock out elbows. Squeeze glutes for lower back."},
                    {"name": "Dumbbell Lateral Raises","sets": "4 sets × 12 reps","rest": "60 sec rest","tip": "Arms at sides, slight elbow bend. Raise to shoulder height, lead with elbows."},
                    {"name": "Front Raises",          "sets": "3 sets × 12 reps","rest": "60 sec rest","tip": "Use plates or dumbbells. Raise to shoulder height. Alternate arms."},
                    {"name": "Arnold Press",          "sets": "3 sets × 10 reps","rest": "60 sec rest","tip": "Start palms facing you at chin, rotate out as you press overhead. Full rotation."},
                    {"name": "Barbell Shrugs",        "sets": "3 sets × 15 reps","rest": "60 sec rest","tip": "Shrug shoulders straight up to ears, hold 1 second. Don't roll shoulders."},
                    {"name": "Rear Delt Flyes",       "sets": "3 sets × 15 reps","rest": "45 sec rest","tip": "Bend over 90°, raise arms to sides. Squeeze rear delts. Pinch shoulder blades."},
                ]
            },
            {
                "day": "Saturday", "label": "Full Body Strength + Core", "type": "training",
                "exercises": [
                    {"name": "Power Cleans",         "sets": "4 sets × 5 reps", "rest": "120 sec rest","tip": "Bar from floor, explosive pull, catch in front rack. Start light — focus on form."},
                    {"name": "Pull-Up Variation",    "sets": "3 sets × 8 reps", "rest": "90 sec rest", "tip": "Wide, close or neutral grip. Full hang to chin above bar. Pause at bottom."},
                    {"name": "Weighted Plank",       "sets": "3 sets × 45 sec", "rest": "45 sec rest", "tip": "Weight plate on lower back. Maintain a straight body position throughout."},
                    {"name": "Cable Woodchop",       "sets": "3 sets × 12/side","rest": "45 sec rest", "tip": "Rotate from high cable to opposite low hip. Core does the work, not arms."},
                    {"name": "Ab Wheel Rollout",     "sets": "3 sets × 10 reps","rest": "45 sec rest", "tip": "Roll forward until arms extended, return by contracting abs. Don't let hips drop."},
                    {"name": "Hanging Leg Raise",    "sets": "3 sets × 12 reps","rest": "45 sec rest", "tip": "Raise legs to 90° or higher. Slow and controlled. Don't swing."},
                ]
            },
            {
                "day": "Sunday", "label": "Full Rest", "type": "rest",
                "exercises": [],
                "note": "Complete rest. Eat your full calorie surplus, sleep 8+ hours. Muscle grows during rest, not during training."
            },
        ],
        "meals": [
            {"time": "Breakfast",     "meal": "Whole eggs, oats & banana",              "detail": "4 whole eggs, 100g oats, 1 banana, 200ml whole milk. High calorie, protein and slow/fast carbs."},
            {"time": "Mid-Morning",   "meal": "Mass shake or peanut butter toast",       "detail": "1 scoop protein, 500ml whole milk, 2 tbsp PB on 2 slices brown bread. Dense calorie hit."},
            {"time": "Lunch",         "meal": "Beef mince with white rice & veg",        "detail": "200g lean beef, 150g white rice, mixed veg. Red meat provides creatine and essential vitamins."},
            {"time": "Pre-Workout",   "meal": "Rice cakes & protein bar",                "detail": "3 rice cakes, 1 quality protein bar (25g+ protein). Quick carbs, no gut discomfort."},
            {"time": "Post-Workout",  "meal": "Protein shake & fruit",                   "detail": "2 scoops whey, 1 banana, 250ml milk. Fast protein and carbs to shuttle nutrients to muscle."},
            {"time": "Dinner",        "meal": "Chicken thighs, pasta & olive oil",       "detail": "250g chicken thighs, 200g pasta, 1 tbsp olive oil. High calorie, protein and fat dense."},
            {"time": "Before Bed",    "meal": "Casein shake or cottage cheese",          "detail": "200g full-fat cottage cheese or 1 scoop casein. Slow protein feeds muscle repair all night."},
        ],
        "avoid": ["Fast food and takeaways — high trans fats impair hormone function", "Alcohol — suppresses testosterone and impairs muscle protein synthesis", "Sugary cereals — cause blood sugar spikes with no muscle-building benefit"],
        "snacks": ["Peanut butter on rice cakes (4–6 cakes)", "Trail mix: almonds, cashews, walnuts, dried mango", "Whole milk blended with banana", "Tuna on wholemeal toast", "Greek yogurt with honey and granola"],
    },

    "cutting": {
        "name": "Cutting — Lean Muscle Retention",
        "icon": "✂️",
        "description": "Strength training to preserve muscle mass with a moderate calorie deficit. High protein prevents muscle breakdown.",
        "style": "Strength + Moderate Cardio",
        "diet_type": "300–500 kcal deficit, high protein",
        "macros": {
            "female": {"kcal": 1600, "protein": 145, "carbs": 140, "fats": 45, "weight": "~65kg"},
            "male":   {"kcal": 2100, "protein": 200, "carbs": 185, "fats": 58, "weight": "~85kg"},
        },
        "macro_rule": "2.2–2.5g protein per kg bodyweight. Deficit of 300–500 calories below TDEE.",
        "days": [
            {
                "day": "Monday", "label": "Upper Body Strength (Push)", "type": "training",
                "exercises": [
                    {"name": "Barbell Bench Press",     "sets": "4 sets × 8 reps", "rest": "75 sec rest","tip": "Maintain strength from bulk. Full range of motion — touch chest and lock out."},
                    {"name": "Incline Dumbbell Press",  "sets": "3 sets × 10 reps","rest": "60 sec rest","tip": "Control the negative — 3 seconds on the way down."},
                    {"name": "Dumbbell Shoulder Press", "sets": "3 sets × 10 reps","rest": "60 sec rest","tip": "Seated for stability. Press from ear height to full extension."},
                    {"name": "Lateral Raises",          "sets": "3 sets × 15 reps","rest": "45 sec rest","tip": "Lighter weight, higher reps to maintain shoulder size. Strict form."},
                    {"name": "Tricep Pushdowns",        "sets": "3 sets × 15 reps","rest": "45 sec rest","tip": "Full extension each rep. Superset with push-ups if time allows."},
                    {"name": "Cable Flyes",             "sets": "3 sets × 12 reps","rest": "45 sec rest","tip": "Squeeze peak contraction for 2 seconds each rep."},
                    {"name": "HIIT Finisher",           "sets": "1 × 10 min",      "rest": "",           "tip": "10 rounds: 30 sec all-out effort (sprints or bike), 30 sec rest."},
                ]
            },
            {
                "day": "Tuesday", "label": "Lower Body Strength", "type": "training",
                "exercises": [
                    {"name": "Barbell Squat",           "sets": "4 sets × 8 reps", "rest": "90 sec rest","tip": "Keep heavy squats to preserve leg muscle. Don't reduce load too aggressively."},
                    {"name": "Romanian Deadlift",       "sets": "3 sets × 10 reps","rest": "75 sec rest","tip": "Full stretch at bottom each rep. 2 sec up, 3 sec down."},
                    {"name": "Bulgarian Split Squats",  "sets": "3 sets × 10/leg", "rest": "60 sec rest","tip": "Rear foot on bench. Lower back knee near floor. Great for quads and balance."},
                    {"name": "Leg Curl Machine",        "sets": "3 sets × 12 reps","rest": "60 sec rest","tip": "Full range. Squeeze at top. 3-second lower. Hamstrings respond to slow reps."},
                    {"name": "Leg Extension",           "sets": "3 sets × 15 reps","rest": "45 sec rest","tip": "Extend fully. Hold 1 second, lower slowly."},
                    {"name": "Calf Raises",             "sets": "3 sets × 20 reps","rest": "30 sec rest","tip": "Full range. Pause at top and bottom."},
                    {"name": "Incline Treadmill Walk",  "sets": "1 × 20 min",      "rest": "",           "tip": "Incline 12–15%, moderate pace. Low-impact fat burning."},
                ]
            },
            {
                "day": "Wednesday", "label": "Active Recovery", "type": "rest",
                "exercises": [],
                "note": "Light activity only. 30-min walk, foam rolling, yoga or swimming. Flexibility work is especially important when calories are lower."
            },
            {
                "day": "Thursday", "label": "Upper Body Strength (Pull)", "type": "training",
                "exercises": [
                    {"name": "Deadlift",                "sets": "3 sets × 5 reps", "rest": "120 sec rest","tip": "Maintain heavy pulling — key signal for muscle retention during a cut."},
                    {"name": "Weighted Pull-Ups",       "sets": "3 sets × 8 reps", "rest": "90 sec rest", "tip": "Full hang to chin over bar. Add belt weight if possible."},
                    {"name": "Seated Cable Row",        "sets": "3 sets × 10 reps","rest": "60 sec rest", "tip": "2 sec pull, 3 sec return. Elbows tight. Feel the lats working."},
                    {"name": "Face Pulls",              "sets": "3 sets × 15 reps","rest": "45 sec rest", "tip": "Critical during a cut for shoulder health. External rotation."},
                    {"name": "Barbell Curl",            "sets": "3 sets × 10 reps","rest": "60 sec rest", "tip": "Maintain bicep training. Slow negative. No swinging."},
                    {"name": "Incline Dumbbell Curl",   "sets": "3 sets × 12 reps","rest": "45 sec rest", "tip": "Full stretch at bottom activates more bicep fibres. Very effective."},
                    {"name": "Cardio",                  "sets": "1 × 25 min",      "rest": "",            "tip": "Moderate jog or bike. Zone 2 heart rate (60–70% max)."},
                ]
            },
            {
                "day": "Friday", "label": "Full Body Circuit", "type": "training",
                "exercises": [
                    {"name": "Squat to Press",          "sets": "4 sets × 12 reps","rest": "45 sec rest","tip": "Dumbbell front squat into overhead press. Burns more calories, multiple muscle groups."},
                    {"name": "Push-Up Variations",      "sets": "3 sets × 15 reps","rest": "45 sec rest","tip": "Mix standard, wide, and close-grip. Higher reps burns calories."},
                    {"name": "Pull-Up or Inverted Row", "sets": "3 sets × 10 reps","rest": "60 sec rest","tip": "For inverted row, lie under bar at 45° and pull chest to bar."},
                    {"name": "Dumbbell Complex",        "sets": "3 sets × 8/movement","rest":"75 sec rest","tip": "6 deadlift, 6 row, 6 curl, 6 press without putting weight down."},
                    {"name": "Hollow Body Hold",        "sets": "3 sets × 30 sec", "rest": "30 sec rest","tip": "Arms overhead, feet 15cm up, lower back pressed flat."},
                    {"name": "Burpee Intervals",        "sets": "3 sets (Tabata)", "rest": "",           "tip": "20 sec max effort, 10 sec rest. 8 rounds. Very effective for fat burning."},
                    {"name": "Stretching",              "sets": "1 × 15 min",      "rest": "",           "tip": "Hold each position 30–45 seconds. Flexibility aids recovery."},
                ]
            },
            {
                "day": "Saturday", "label": "Cardio & Core", "type": "training",
                "exercises": [
                    {"name": "Outdoor Run or Cycle",   "sets": "1 × 35 min",      "rest": "",           "tip": "Steady-state Zone 2. Conversational pace. Burns fat without muscle breakdown."},
                    {"name": "Plank Variations",       "sets": "3 sets × 45 sec each","rest": "30 sec rest","tip": "Standard, side plank each side, reverse plank. Increase hold time each week."},
                    {"name": "Dead Bug",               "sets": "3 sets × 10/side","rest": "30 sec rest","tip": "Opposite arm and leg lower together. Back stays flat. Deep core stability."},
                    {"name": "Cable Woodchop",         "sets": "3 sets × 12/side","rest": "30 sec rest","tip": "Rotate through torso. Builds oblique definition safely."},
                    {"name": "Lying Leg Raise",        "sets": "3 sets × 15 reps","rest": "30 sec rest","tip": "Lower back stays on floor. Legs lower slowly without touching floor."},
                    {"name": "Foam Rolling",           "sets": "1 × 15 min",      "rest": "",           "tip": "Cover all major groups: quads, hamstrings, lats, calves, thoracic spine."},
                ]
            },
            {
                "day": "Sunday", "label": "Full Rest", "type": "rest",
                "exercises": [],
                "note": "Complete rest. Eat your full calorie target, sleep 7–9 hours. Do not add extra cardio on rest days during a cut."
            },
        ],
        "meals": [
            {"time": "Breakfast",     "meal": "Egg white omelette with spinach & toast",   "detail": "6 egg whites (2 whole), large handful spinach, 1–2 slices wholemeal toast."},
            {"time": "Mid-Morning",   "meal": "Protein shake & fruit",                      "detail": "1 scoop whey in water, 1 apple. Keeps protein high without excess calories."},
            {"time": "Lunch",         "meal": "Turkey breast with brown rice & steamed veg","detail": "200g turkey, 80g dry brown rice, 200g veg. Lean protein, complex carbs, high volume."},
            {"time": "Pre-Workout",   "meal": "Banana & protein shake",                     "detail": "1 banana, half scoop protein. Carbs for energy, protein to protect muscle."},
            {"time": "Post-Workout",  "meal": "Chicken breast & sweet potato",              "detail": "180g chicken, 150g sweet potato. Replenish glycogen, spike muscle protein synthesis."},
            {"time": "Dinner",        "meal": "White fish with asparagus & green beans",    "detail": "220g cod or tilapia, 150g asparagus, green beans. Very low calorie, very high protein."},
            {"time": "Evening",       "meal": "Casein protein or cottage cheese",           "detail": "1 scoop casein or 150g cottage cheese. Slow protein prevents overnight muscle breakdown."},
        ],
        "avoid": ["High calorie condiments: mayo, full-fat dressings, creamy sauces", "Liquid calories: juice, smoothies, lattes", "White bread, white pasta, white rice (except post-workout)", "Cheese and full-fat dairy — very calorie dense", "Alcohol — 7 kcal/g, no nutritional value, impairs fat burning for 24+ hours"],
        "snacks": ["Celery with almond butter (1 tbsp)", "Boiled eggs — 2 to 3 with hot sauce", "Edamame — high protein and low calorie", "Turkey slices rolled with cucumber", "Low-calorie protein pudding"],
    },

    "shredding": {
        "name": "Shredding — Competition Ready",
        "icon": "⚡",
        "description": "Aggressive deficit, twice-daily training, carb cycling and extreme dietary discipline. Not suitable for beginners.",
        "style": "Twice-Daily + Carb Cycling",
        "diet_type": "Aggressive deficit + carb cycle",
        "macros": {
            "female": {"kcal": 1300, "protein": 150, "carbs": 90,  "fats": 35, "weight": "~60kg"},
            "male":   {"kcal": 1750, "protein": 210, "carbs": 130, "fats": 48, "weight": "~80kg"},
        },
        "macro_rule": "High Carb Days (Training): Add 150–200g carbs around workouts. Low Carb Days (Rest): Reduce carbs 100–150g, increase protein slightly.",
        "days": [
            {
                "day": "Monday", "label": "Morning Legs | Evening LISS Cardio", "type": "double",
                "exercises": [
                    {"name": "Barbell Squat",        "sets": "5 sets × 5 reps", "rest": "120 sec rest","tip": "Maintain heavy strength. Preserves muscle on an aggressive deficit."},
                    {"name": "Leg Press",            "sets": "4 sets × 12 reps","rest": "75 sec rest", "tip": "High volume after heavy squats. Full range. Don't lock knees at top."},
                    {"name": "Hack Squat",           "sets": "3 sets × 15 reps","rest": "60 sec rest", "tip": "Quad isolation. Feet forward, close together. The quad burn should be intense."},
                    {"name": "Romanian Deadlift",    "sets": "4 sets × 10 reps","rest": "75 sec rest", "tip": "Hamstring focus. Controlled tempo. Feel the full stretch at bottom."},
                    {"name": "Lying Leg Curl",       "sets": "4 sets × 12 reps","rest": "60 sec rest", "tip": "Squeeze hard at top. 3-second negative. Hamstrings critical for leg shape."},
                    {"name": "Seated Calf Raises",   "sets": "4 sets × 25 reps","rest": "30 sec rest", "tip": "Seated for soleus. Full range, pause at top. High volume and frequency needed."},
                    {"name": "Evening: Incline Treadmill Walk","sets": "45 min","rest": "","tip": "12–15% incline, 5.5–6 km/h. Maximum fat burning zone. Do not hold handrails."},
                ]
            },
            {
                "day": "Tuesday", "label": "Morning Chest & Triceps | Evening HIIT", "type": "double",
                "exercises": [
                    {"name": "Flat Bench Press",              "sets": "4 sets × 8 reps", "rest": "75 sec rest","tip": "3-second negative for maximum muscle fibre engagement in a deficit."},
                    {"name": "Incline Dumbbell Press",        "sets": "3 sets × 12 reps","rest": "60 sec rest","tip": "Controlled tempo. No bouncing off chest."},
                    {"name": "Pec Deck / Cable Fly",          "sets": "3 sets × 15 reps","rest": "45 sec rest","tip": "Full peak contraction. 2-second hold at squeeze. Arms arc, they don't press."},
                    {"name": "Close Grip Bench Press",        "sets": "3 sets × 10 reps","rest": "60 sec rest","tip": "Hands 30cm apart. Elbows tight to ribs. Primary tricep compound."},
                    {"name": "Overhead Tricep Extension",     "sets": "3 sets × 12 reps","rest": "45 sec rest","tip": "Both hands on one dumbbell overhead. Full range every rep."},
                    {"name": "Tricep Pushdowns Drop Set",     "sets": "3 sets × 12 reps","rest": "30 sec rest","tip": "Heavy 10, drop 20%, 10 more, drop 20%, to failure. Extreme for definition."},
                    {"name": "Evening: Sprint Intervals",     "sets": "8 rounds",        "rest": "",           "tip": "30 sec max sprint, 90 sec rest. Go all out every sprint."},
                ]
            },
            {
                "day": "Wednesday", "label": "Back, Biceps & Core", "type": "training",
                "exercises": [
                    {"name": "Deadlift",                "sets": "4 sets × 5 reps", "rest": "120 sec rest","tip": "Maintain this lift at all costs during a shred. Greatest muscle engagement per rep."},
                    {"name": "Weighted Pull-Ups",       "sets": "4 sets × 8 reps", "rest": "90 sec rest", "tip": "Full hang, chin over bar. Best lat builder for a shredded physique."},
                    {"name": "T-Bar Row",               "sets": "3 sets × 10 reps","rest": "75 sec rest", "tip": "Mid-back thickness. Elbows drive back, not up. Chest on pad."},
                    {"name": "Wide Lat Pulldown",       "sets": "3 sets × 12 reps","rest": "60 sec rest", "tip": "Wide overhand grip. Pull to upper chest, lean back slightly. Full stretch at top."},
                    {"name": "Incline Dumbbell Curl",   "sets": "3 sets × 12 reps","rest": "60 sec rest", "tip": "Full stretch activates more fibres. Supinate as you curl. Squeeze at top."},
                    {"name": "Concentration Curl",      "sets": "3 sets × 15 reps","rest": "45 sec rest", "tip": "Elbow on inner thigh. Curl slowly to peak. Best for bicep peak development."},
                    {"name": "Plank to Pike",           "sets": "3 sets × 10 reps","rest": "45 sec rest", "tip": "From plank, push hips to sky (downward dog), return. Intense core and shoulder."},
                    {"name": "V-Ups",                   "sets": "3 sets × 15 reps","rest": "30 sec rest", "tip": "Raise arms and legs simultaneously to form a V. Keep both straight if possible."},
                ]
            },
            {
                "day": "Thursday", "label": "Morning Shoulders | Evening LISS Cardio", "type": "double",
                "exercises": [
                    {"name": "Seated Dumbbell Press",    "sets": "4 sets × 8 reps",  "rest": "75 sec rest","tip": "Heavy overhead pressing to retain shoulder mass."},
                    {"name": "Arnold Press",             "sets": "3 sets × 10 reps", "rest": "60 sec rest","tip": "Rotation gives full deltoid engagement. Very effective for roundness."},
                    {"name": "Lateral Raise Drop Set",   "sets": "3 sets",           "rest": "45 sec rest","tip": "Standard weight to failure, drop 20%, to failure, drop 20%, to failure."},
                    {"name": "Cable Lateral Raise",      "sets": "3 sets × 15/arm",  "rest": "30 sec rest","tip": "One arm at a time. Constant cable tension superior to dumbbells for separation."},
                    {"name": "Reverse Pec Deck",         "sets": "3 sets × 15 reps", "rest": "45 sec rest","tip": "Rear delt isolation. Essential for balanced shoulder development."},
                    {"name": "Barbell Shrugs",           "sets": "3 sets × 20 reps", "rest": "45 sec rest","tip": "Higher reps during a shred. Keep traps engaged. Straight up."},
                    {"name": "Evening: Cycling or Swimming","sets": "45 min",        "rest": "",           "tip": "Moderate pace. Low impact, ideal for recovery from heavy lifting."},
                ]
            },
            {
                "day": "Friday", "label": "Full Body Metabolic Circuit", "type": "training",
                "exercises": [
                    {"name": "Barbell Complex",          "sets": "5 sets × 6/movement","rest": "90 sec rest","tip": "6 deadlift, 6 bent row, 6 hang clean, 6 front squat, 6 press. Do NOT put bar down."},
                    {"name": "Dumbbell Thruster",        "sets": "4 sets × 12 reps",   "rest": "60 sec rest","tip": "DB front squat into overhead press. One of the highest calorie burn exercises per minute."},
                    {"name": "Pull-Up to Knee Raise",    "sets": "3 sets × 10 reps",   "rest": "75 sec rest","tip": "Full pull-up, hold, raise knees to chest, lower. Extreme core and back."},
                    {"name": "Box Jump to Step Down",    "sets": "4 sets × 10 reps",   "rest": "60 sec rest","tip": "Explode onto box. Step down — do not jump — to protect the Achilles."},
                    {"name": "Renegade Row Push-Up",     "sets": "3 sets × 8/side",    "rest": "60 sec rest","tip": "Push-up, row left, push-up, row right. Hips must stay perfectly still."},
                    {"name": "Hollow Body Hold",         "sets": "3 sets × 45 sec",    "rest": "30 sec rest","tip": "Arms extended back, legs 15cm up, lower back pressed flat. Core endurance essential."},
                ]
            },
            {
                "day": "Saturday", "label": "Morning HIIT | Afternoon Flexibility", "type": "double",
                "exercises": [
                    {"name": "Sprint or Assault Bike",  "sets": "10 rounds",  "rest": "",           "tip": "40 sec max effort, 20 sec rest. Absolute maximum every round. No holding back."},
                    {"name": "Burpee Intervals",        "sets": "5 rounds",   "rest": "",           "tip": "20 sec on, 10 sec off. Tabata protocol. One of the most effective fat burning protocols."},
                    {"name": "Afternoon: Yoga / Full Stretch","sets": "45 min","rest": "",          "tip": "Hip flexors, hamstrings, quads, shoulders, chest. Hold 45–60 sec each."},
                ]
            },
            {
                "day": "Sunday", "label": "Full Rest — Mandatory", "type": "rest",
                "exercises": [],
                "note": "Complete rest. Not optional. Twice-daily sessions require a full rest day for CNS recovery. Sleep, eat well, prepare for next week."
            },
        ],
        "meals": [
            {"time": "Breakfast (Training)", "meal": "Egg whites, oats & berries", "detail": "8 egg whites, 80g oats, 100g blueberries. High protein and complex carbs for hard training."},
            {"time": "Mid-Morning",          "meal": "Protein shake & rice cakes",  "detail": "1.5 scoops whey, 4 rice cakes with almond butter. Sustained energy."},
            {"time": "Lunch",                "meal": "Chicken and rice",             "detail": "220g chicken, 150g white rice, broccoli, soy sauce. Classic shredding meal."},
            {"time": "Pre-Workout",          "meal": "Banana & BCAAs",              "detail": "1 banana, 10g BCAAs in water. Simple carbs spike energy. BCAAs protect muscle."},
            {"time": "Post-Workout",         "meal": "Whey & dextrose",             "detail": "2 scoops whey, 50g dextrose in water. Immediate muscle protein synthesis."},
            {"time": "Dinner",               "meal": "Turkey & sweet potato",       "detail": "200g turkey mince, 150g sweet potato, asparagus. Moderate carbs, very high protein."},
            {"time": "Pre-Sleep",            "meal": "Casein shake",                "detail": "1.5 scoops casein in water. 7–8 hours of slow-release amino acids."},
        ],
        "avoid": ["Any added sugar in any form", "Alcohol — eliminates fat burning for 24–48 hours", "Fruit juice — liquid fructose stalls fat loss", "Bread, pasta and cereals on rest days", "Cheat meals — even one can set back a week of progress", "High-sodium processed foods — causes water retention"],
        "snacks": ["Almonds and string cheese (30g almonds, 2 sticks)", "Tuna salad with olive oil and avocado", "Protein shake in water only", "Cottage cheese and walnuts (150g + 20g)", "Celery with almond butter"],
        "supplements": ["Whey Protein Isolate — 2–3 servings daily", "BCAAs — intra-workout on low carb days", "Creatine Monohydrate — 5g daily", "Caffeine or pre-workout", "Omega-3 Fish Oil — 3g daily", "Vitamin D and Zinc"],
    }
}

# ─── TDEE calculation ──────────────────────────────────────────────────────────

def calculate_tdee(gender, age, height_cm, weight_kg, days_per_week):
    # Mifflin-St Jeor BMR
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # Activity multiplier
    multipliers = {3: 1.375, 4: 1.55, 5: 1.55, 6: 1.725, 7: 1.9}
    multiplier = multipliers.get(int(days_per_week), 1.375)
    return round(bmr * multiplier)


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if request.method == 'POST':
        data = request.form.to_dict()
        session['user'] = data
        return redirect(url_for('plan'))
    return render_template('onboarding.html')


@app.route('/plan')
def plan():
    user = session.get('user')
    if not user:
        return redirect(url_for('onboarding'))

    goal_map = {
        "weight_loss": "weight_loss",
        "bulking": "bulking",
        "cutting": "cutting",
        "shredding": "shredding",
    }
    goal_key = goal_map.get(user.get('goal'), 'weight_loss')
    plan_data = PLANS[goal_key]

    # Parse measurements
    try:
        weight = float(user.get('weight', 75))
        height = float(user.get('height', 170))
        age    = int(user.get('age', 25))
        days   = int(user.get('days', 4))
    except (ValueError, TypeError):
        weight, height, age, days = 75, 170, 25, 4

    gender_raw = user.get('gender', 'male').lower()
    gender = 'male' if gender_raw in ('male', 'm') else 'female'

    tdee = calculate_tdee(gender, age, height, weight, days)

    # Recommended calories
    macros_key = 'male' if gender == 'male' else 'female'
    macros = plan_data['macros'][macros_key]

    return render_template('plan.html',
                           user=user,
                           plan=plan_data,
                           goal_key=goal_key,
                           tdee=tdee,
                           macros=macros,
                           gender=gender)


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
