"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from pymongo import MongoClient
from typing import Dict, Any

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# MongoDB setup
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mergington_high_school"]
    activities_collection = db["activities"]
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    raise e

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Get all activities from MongoDB"""
    try:
        activities_cursor = activities_collection.find({})
        activities = {}

        for activity in activities_cursor:
            activity_name = activity["_id"]
            # Remove MongoDB's _id and name fields, keep the rest
            activity_data = {k: v for k, v in activity.items() if k not in [
                "_id", "name"]}
            activities[activity_name] = activity_data

        return activities
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")


@app.get("/debug/activities")
def debug_activities():
    """Debug endpoint to check activities data from MongoDB"""
    try:
        activities_cursor = activities_collection.find({})
        all_activities = {}

        for activity in activities_cursor:
            activity_name = activity["_id"]
            activity_data = {k: v for k, v in activity.items() if k not in [
                "_id", "name"]}
            all_activities[activity_name] = activity_data

        return {
            "total_activities": len(all_activities),
            "sample_activity": list(all_activities.items())[0] if all_activities else None,
            "all_activities": all_activities
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity using MongoDB"""
    try:
        # Find the activity
        activity = activities_collection.find_one({"_id": activity_name})

        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Check if student is already signed up
        if email in activity["participants"]:
            raise HTTPException(
                status_code=400, detail="Student is already signed up for this activity")

        # Check if activity is full
        if len(activity["participants"]) >= activity["max_participants"]:
            raise HTTPException(status_code=400, detail="Activity is full")

        # Add participant to the activity
        result = activities_collection.update_one(
            {"_id": activity_name},
            {"$push": {"participants": email}}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=500, detail="Failed to sign up for activity")

        return {"message": f"Successfully signed up {email} for {activity_name}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")


@app.delete("/activities/{activity_name}/participant/{email}")
def remove_participant(activity_name: str, email: str):
    """Remove a participant from an activity using MongoDB"""
    try:
        # Find the activity
        activity = activities_collection.find_one({"_id": activity_name})

        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Check if participant exists
        if email not in activity["participants"]:
            raise HTTPException(
                status_code=404, detail="Participant not found in this activity")

        # Remove participant from the activity
        result = activities_collection.update_one(
            {"_id": activity_name},
            {"$pull": {"participants": email}}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=500, detail="Failed to remove participant")

        return {"message": f"Successfully removed {email} from {activity_name}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")
