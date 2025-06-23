#!/usr/bin/env python3
"""
Database Population Script

This script populates the MongoDB database with initial activities data.
"""

from pymongo import MongoClient
import json

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["mergington_high_school"]
activities_collection = db["activities"]

# Initial activities data
activities_data = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Join the school basketball team and compete in tournaments",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swimming lessons and competitive swimming events",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["james@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art mediums including painting, drawing, and sculpture",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["emily@mergington.edu", "lucas@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, theater production, and performance arts",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["mia@mergington.edu", "noah@mergington.edu", "ava@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop critical thinking and public speaking skills through competitive debates",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["liam@mergington.edu", "isabella@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Compete in various science and engineering challenges",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 24,
        "participants": ["ethan@mergington.edu", "charlotte@mergington.edu", "mason@mergington.edu"]
    }
}


def populate_database():
    """Populate the database with initial activities data."""
    try:
        # Clear existing data
        activities_collection.delete_many({})
        print("Cleared existing activities data")

        # Insert activities data
        for activity_name, activity_data in activities_data.items():
            document = {
                "_id": activity_name,  # Use activity name as the _id
                "name": activity_name,
                **activity_data
            }
            activities_collection.insert_one(document)
            print(f"Inserted activity: {activity_name}")

        print(
            f"\nSuccessfully populated database with {len(activities_data)} activities")

        # Verify the data was inserted
        count = activities_collection.count_documents({})
        print(f"Total activities in database: {count}")

        # Show sample data
        sample = activities_collection.find_one()
        if sample:
            print(f"\nSample activity document:")
            print(json.dumps(sample, indent=2, default=str))

    except Exception as e:
        print(f"Error populating database: {e}")
        return False

    return True


if __name__ == "__main__":
    print("Populating MongoDB with activities data...")
    success = populate_database()
    if success:
        print("\n✅ Database population completed successfully!")
    else:
        print("\n❌ Database population failed!")
