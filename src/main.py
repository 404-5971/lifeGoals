from flask import Flask, render_template, request, redirect, url_for, Response as FlaskResponse, make_response
import werkzeug.wrappers
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from typing import TypedDict, Optional

app = Flask(__name__)

GOALS_FILE = "lifeGoals.txt"
GOALS_METADATA_FILE = "lifeGoals_metadata.json"

class GoalMetadata(TypedDict):
    """
    date: str # %d/%m/%Y
    time: str # %H:%M:%S
    timezone: str # %z
    """
    goal: str
    completed: bool
    date: Optional[str]
    time: Optional[str]
    timezone: Optional[str]

def load_goals() -> list[str]:
    try:
        with open(GOALS_FILE, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def load_goals_by_category() -> dict[str, list[str]]:
    """Parse the goals file into a dict of {category: [goals]}"""
    goals_by_cat: dict[str, list[str]] = {}
    current_cat = None
    try:
        with open(GOALS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("[") and line.endswith("]"):
                    current_cat = line[1:-1].strip()
                    if current_cat not in goals_by_cat:
                        goals_by_cat[current_cat] = []
                elif current_cat:
                    goals_by_cat[current_cat].append(line)
        return goals_by_cat
    except FileNotFoundError:
        return {}

def load_goals_metadata() -> list[GoalMetadata]:
    try:
        with open(GOALS_METADATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        with open(GOALS_METADATA_FILE, "w") as file:
            json.dump([], file)
        return load_goals_metadata()

def save_goals_metadata(goals_metadata: list[GoalMetadata]) -> None:
    with open(GOALS_METADATA_FILE, "w") as file:
        json.dump(goals_metadata, file, indent=2)

def add_goals_metadata() -> None:
    goals_by_cat = load_goals_by_category()
    all_goals = [goal for goals in goals_by_cat.values() for goal in goals]
    goals_metadata: list[GoalMetadata] = load_goals_metadata()
    existing_goals_with_metadata: set[Optional[str]] = {meta.get('goal') for meta in goals_metadata}
    for goal in all_goals:
        if goal not in existing_goals_with_metadata:
            goals_metadata.append(GoalMetadata(goal=goal, completed=False, date=None, time=None, timezone=None))
    save_goals_metadata(goals_metadata)

@app.route("/", methods=["GET"])
def index() -> FlaskResponse:
    goals_by_cat = load_goals_by_category()
    categories = list(goals_by_cat.keys())
    selected_category = request.args.get("category") or (categories[0] if categories else None)
    goals = goals_by_cat.get(selected_category, []) if selected_category else []
    goals_metadata: list[GoalMetadata] = load_goals_metadata()
    add_goals_metadata()
    resp = make_response(render_template(
        "index.html",
        categories=categories,
        selected_category=selected_category,
        goals=goals,
        goals_metadata=goals_metadata
    ))
    # Set user_tz cookie if not present (will be set by JS on client if missing)
    return resp

@app.route("/complete", methods=["POST"])
def complete_goal() ->  werkzeug.wrappers.Response:
    goal: Optional[str] = request.form.get("goal")
    category: Optional[str] = request.form.get("category")
    if goal is None:
        return redirect(url_for("index"))
    now: datetime = datetime.now(ZoneInfo("UTC")).astimezone()
    goals_metadata: list[GoalMetadata] = load_goals_metadata()
    for goal_metadata in goals_metadata:
        if goal_metadata["goal"] == goal:
            if goal_metadata["completed"]:
                goal_metadata["completed"] = False
                goal_metadata["date"] = None
                goal_metadata["time"] = None
                goal_metadata["timezone"] = None
            else:
                goal_metadata["completed"] = True
                goal_metadata["date"] = now.strftime("%d/%m/%Y")
                goal_metadata["time"] = now.strftime("%H:%M:%S")
                goal_metadata["timezone"] = now.strftime("%z")
                if goal_metadata["timezone"]:
                    goal_metadata["timezone"] = f"{goal_metadata['timezone'][:3]}:{goal_metadata['timezone'][3:]}"
    save_goals_metadata(goals_metadata)
    if category:
        return redirect(url_for("index", category=category))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
