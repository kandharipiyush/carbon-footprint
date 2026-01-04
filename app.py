from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    transport_km = float(request.form["transport"])
    electricity_units = float(request.form["electricity"])
    food_type = request.form["food"]
    period = request.form["period"]

    # Base daily emissions
    transport_em = transport_km * 0.21
    electricity_em = electricity_units * 0.82
    food_em = 1.5 if food_type == "veg" else 2.5 if food_type == "mixed" else 3.5

    total = transport_em + electricity_em + food_em

    # Monthly conversion
    if period == "monthly":
        transport_em *= 30
        electricity_em *= 30
        food_em *= 30
        total *= 30

    # Rounding
    transport_em = round(transport_em, 2)
    electricity_em = round(electricity_em, 2)
    food_em = round(food_em, 2)
    total = round(total, 2)

    # 🔑 Normalized score (daily-equivalent)
    score_base = total / 30 if period == "monthly" else total

    if score_base < 5:
        score, score_color = "Low 🌱 (Eco-friendly)", "green"
    elif score_base < 10:
        score, score_color = "Medium ⚠️ (Needs improvement)", "orange"
    else:
        score, score_color = "High 🚨 (Immediate action needed)", "red"

    badge = "🌱 Eco Starter" if score_base < 4 else "🌿 Eco Aware" if score_base < 8 else "🔥 High Emitter"

    # Percentage contribution
    transport_pct = round((transport_em / total) * 100, 1)
    electricity_pct = round((electricity_em / total) * 100, 1)
    food_pct = round((food_em / total) * 100, 1)

    # Highest source
    max_source = max(
        ("Transport", transport_em),
        ("Electricity", electricity_em),
        ("Food", food_em),
        key=lambda x: x[1]
    )[0]

    facts = {
        "Transport": "Private vehicles are among the fastest-growing CO₂ sources.",
        "Electricity": "Air conditioners can consume up to 5× more power than fans.",
        "Food": "Meat-based diets generate significantly higher emissions."
    }

    action_plan = [
        "Reduce daily commute by 2 km or carpool",
        "Lower AC usage by 1 hour per day",
        "Add 1–2 meat-free days per week"
    ]

    # Savings & offsets
    co2_saved = round(total * 0.15, 2)
    money_saved = round(co2_saved * 50)
    trees = round(total / 21, 1)
    weekly_goal = round(total * 0.9, 2)

    # 🌍 Carbon Shadow (Future Impact)
    yearly_emission = round(score_base * 365, 2)
    trees_year = round(yearly_emission / 21, 1)

    benchmark = "Within recommended range" if score_base <= 8 else "Above recommended average"
    timestamp = datetime.now().strftime("%d %b %Y, %H:%M")

    return render_template(
        "result.html",
        transport=transport_em,
        electricity=electricity_em,
        food=food_em,
        total=total,
        score=score,
        score_color=score_color,
        badge=badge,
        transport_pct=transport_pct,
        electricity_pct=electricity_pct,
        food_pct=food_pct,
        max_source=max_source,
        fact=facts[max_source],
        action_plan=action_plan,
        co2_saved=co2_saved,
        money_saved=money_saved,
        trees=trees,
        weekly_goal=weekly_goal,
        yearly_emission=yearly_emission,
        trees_year=trees_year,
        benchmark=benchmark,
        period=period.capitalize(),
        timestamp=timestamp
    )

if __name__ == "__main__":
    app.run(debug=True)
