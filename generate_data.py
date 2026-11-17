
import pandas as pd
import numpy as np
import uuid
from faker import Faker
import random
import os

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)
Faker.seed(42)

# Project configuration
START_DATE = "2022-01-01"
END_DATE = "2026-12-31"

OUTPUT_FOLDER = "data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def generate_uuid():
    return str(uuid.uuid4())


print("Hospitality data generation started...")


# 1. Generate Hotels and Rooms

hotel_locations = {
    "Goa": ["Beach Resort", "Luxury Resort"],
    "Jaipur": ["Heritage Hotel", "Boutique Hotel"],
    "Ooty": ["Hill Resort", "Nature Retreat"],
    "Bengaluru": ["Business Hotel", "City Hotel"],
    "Chennai": ["Business Hotel", "Luxury Hotel"]
}

hotels = []
rooms = []

for city, hotel_types in hotel_locations.items():
    for hotel_type in hotel_types:
        hotel_id = generate_uuid()

        hotel = {
            "hotel_id": hotel_id,
            "hotel_name": f"{fake.last_name()} {hotel_type}",
            "location": city,
            "hotel_type": hotel_type,
            "room_capacity": 0
        }

        hotels.append(hotel)

        room_types = ["Standard", "Deluxe", "Suite"]

        for room_type in room_types:
            count = random.randint(10, 20)

            for i in range(count):
                rooms.append({
                    "room_id": generate_uuid(),
                    "hotel_id": hotel_id,
                    "room_type": room_type,
                    "room_number": f"{room_type[:1]}{len(rooms) + 1:03d}"
                })

# Match hotel capacity with actual generated rooms
for hotel in hotels:
    hotel["room_capacity"] = sum(
        1 for room in rooms
        if room["hotel_id"] == hotel["hotel_id"]
    )

df_hotels = pd.DataFrame(hotels)
df_rooms = pd.DataFrame(rooms)

df_hotels.to_csv(f"{OUTPUT_FOLDER}/dim_hotel.csv", index=False)
df_rooms.to_csv(f"{OUTPUT_FOLDER}/dim_room.csv", index=False)

print("Hotels and rooms generated.")
print("Total hotels:", len(df_hotels))
print("Total rooms:", len(df_rooms))


# 2. Generate Guests

guests = []

for _ in range(1000):
    guests.append({
        "guest_id": generate_uuid(),
        "guest_name": fake.name(),
        "guest_type": random.choice(["Business", "Leisure", "Family"]),
        "country": random.choice([
            "India", "USA", "UK", "Australia",
            "Germany", "France", "Singapore"
        ])
    })

df_guests = pd.DataFrame(guests)
df_guests.to_csv(f"{OUTPUT_FOLDER}/dim_guest.csv", index=False)


# 3. Generate Employees

employees = []

for hotel in hotels:
    employee_count = random.randint(20, 40)

    for _ in range(employee_count):
        employees.append({
            "employee_id": generate_uuid(),
            "employee_name": fake.name(),
            "position": random.choice([
                "Manager", "Receptionist", "Chef",
                "Housekeeping Staff", "Security",
                "Waiter", "Maintenance Staff"
            ]),
            "department": random.choice([
                "Management", "Front Office",
                "Food and Beverage", "Housekeeping",
                "Security", "Maintenance"
            ]),
            "hotel_id": hotel["hotel_id"]
        })

df_employees = pd.DataFrame(employees)
df_employees.to_csv(f"{OUTPUT_FOLDER}/dim_employee.csv", index=False)

print("Guests and employees generated.")
print("Total guests:", len(df_guests))
print("Total employees:", len(df_employees))


# 4. Generate Date Dimension

dates = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="D"
)

date_records = []

for date in dates:
    month = date.month

    if month in [12, 1, 2]:
        season = "Winter"
    elif month in [3, 4, 5, 6]:
        season = "Summer"
    elif month in [7, 8, 9]:
        season = "Monsoon"
    else:
        season = "Post-Monsoon"

    date_records.append({
        "date_id": int(date.strftime("%Y%m%d")),
        "full_date": date.date(),
        "day": date.day,
        "month": month,
        "month_name": date.strftime("%B"),
        "quarter": date.quarter,
        "year": date.year,
        "season": season
    })

df_dates = pd.DataFrame(date_records)

df_dates.to_csv(
    f"{OUTPUT_FOLDER}/dim_date.csv",
    index=False
)

print("Date dimension generated.")
print("Total dates:", len(df_dates))


# 5. Generate Room Night Fact Data

room_nights = []

for hotel in hotels:
    hotel_rooms = [
        room for room in rooms
        if room["hotel_id"] == hotel["hotel_id"]
    ]

    city = hotel["location"]

    for date in dates:
        month = date.month

        # Base occupancy by city and season
        if city == "Goa":
            occupancy_rate = (
                0.65 if month in [11, 12, 1, 2] else 0.45
            )

        elif city == "Jaipur":
            occupancy_rate = (
                0.70 if month in [10, 11, 12, 1, 2] else 0.45
            )

        elif city == "Ooty":
            occupancy_rate = (
                0.70 if month in [4, 5, 6] else 0.45
            )

        elif city == "Bengaluru":
            occupancy_rate = (
                0.70 if date.weekday() < 5 else 0.50
            )

        else:
            occupancy_rate = (
                0.65 if date.weekday() < 5 else 0.45
            )

        for room in hotel_rooms:
            is_available = random.random() > 0.03

            is_occupied = (
                is_available and random.random() < occupancy_rate
            )

            # Room pricing by room type
            base_price = {
                "Standard": 2500,
                "Deluxe": 4000,
                "Suite": 7000
            }[room["room_type"]]

            # Seasonal ADR variation
            seasonal_factor = 1.0

            if month in [4, 5, 12]:
                seasonal_factor = 1.25

            elif month in [6, 7, 8, 9]:
                seasonal_factor = 0.85

            room_revenue = 0

            if is_occupied:
                room_revenue = round(
                    base_price
                    * seasonal_factor
                    * random.uniform(0.9, 1.1),
                    2
                )

            room_nights.append({
                "room_night_id": generate_uuid(),
                "hotel_id": hotel["hotel_id"],
                "room_id": room["room_id"],
                "date_id": int(date.strftime("%Y%m%d")),
                "is_available": int(is_available),
                "is_occupied": int(is_occupied),
                "room_revenue": room_revenue
            })

df_room_nights = pd.DataFrame(room_nights)

df_room_nights.to_csv(
    f"{OUTPUT_FOLDER}/fact_room_night.csv",
    index=False
)

print("Room night data generated.")
print("Total room night records:", len(df_room_nights))


# 6. Generate Guest Feedback

feedback_records = []

for _ in range(5000):
    guest = random.choice(guests)
    hotel = random.choice(hotels)
    feedback_date = random.choice(dates)

    # General satisfaction distribution
    rating = random.choices(
        [1, 2, 3, 4, 5],
        weights=[2, 4, 14, 40, 40]
    )[0]

    # Slightly lower satisfaction during selected busy periods
    if feedback_date.month in [4, 5, 12]:
        rating = max(
            1,
            rating - random.choice([0, 0, 1])
        )

    feedback_records.append({
        "feedback_id": generate_uuid(),
        "guest_id": guest["guest_id"],
        "hotel_id": hotel["hotel_id"],
        "date_id": int(feedback_date.strftime("%Y%m%d")),
        "satisfaction_rating": rating
    })

df_feedback = pd.DataFrame(feedback_records)

df_feedback.to_csv(
    f"{OUTPUT_FOLDER}/fact_guest_feedback.csv",
    index=False
)


# 7. Generate Employee Movement

movement_records = []

# Higher exit probability during selected post-peak periods
seasonal_exit_probabilities = {
    1: 0.08,
    2: 0.08,
    3: 0.12,
    4: 0.08,
    5: 0.08,
    6: 0.08,
    7: 0.10,
    8: 0.10,
    9: 0.12,
    10: 0.08,
    11: 0.08,
    12: 0.08
}

for employee in employees:
    hotel_id = employee["hotel_id"]

    # Every employee has a joining event
    join_date = random.choice(dates)

    movement_records.append({
        "movement_id": generate_uuid(),
        "employee_id": employee["employee_id"],
        "hotel_id": hotel_id,
        "date_id": int(join_date.strftime("%Y%m%d")),
        "movement_type": "JOIN"
    })

    # Exit probability depends on the employee's joining month
    # and the selected seasonal employment assumptions
    exit_probability = seasonal_exit_probabilities[join_date.month]

    if random.random() < exit_probability:

        possible_exit_dates = dates[
            dates > join_date
        ]

        if len(possible_exit_dates) > 0:

            # Exits are more likely in selected post-peak months
            preferred_dates = possible_exit_dates[
                possible_exit_dates.month.isin([3, 7, 9])
            ]

            if len(preferred_dates) > 0:
                exit_date = random.choice(preferred_dates)
            else:
                exit_date = random.choice(possible_exit_dates)

            movement_records.append({
                "movement_id": generate_uuid(),
                "employee_id": employee["employee_id"],
                "hotel_id": hotel_id,
                "date_id": int(exit_date.strftime("%Y%m%d")),
                "movement_type": "EXIT"
            })

df_movements = pd.DataFrame(movement_records)

df_movements.to_csv(
    f"{OUTPUT_FOLDER}/fact_employee_movement.csv",
    index=False
)

print("Guest feedback and employee movement generated.")
print("Total feedback records:", len(df_feedback))
print("Total employee movement records:", len(df_movements))

print("\nAll data generation completed!")
