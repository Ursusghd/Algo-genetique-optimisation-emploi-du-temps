from .models import Professor, Room, Course, TimeSlot
import random

def generate_sample_data():
    professors = [
        Professor(1, "Dr. Smith"),
        Professor(2, "Dr. Jones"),
        Professor(3, "Dr. Brown"),
        Professor(4, "Dr. Wilson"),
    ]
    
    rooms = [
        Room(1, "Hall A", 50),
        Room(2, "Lab 1", 20),
        Room(3, "Hall B", 100),
    ]
    
    courses = [
        Course(1, "Mathematics", professors[0], 45),
        Course(2, "Physics", professors[1], 30),
        Course(3, "Computer Science", professors[2], 25),
        Course(4, "Biology", professors[3], 60),
        Course(5, "Chemistry", professors[1], 15),
        Course(6, "History", professors[0], 40),
    ]
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    hours = ["08:00", "10:00", "14:00", "16:00"]
    
    timeslots = []
    ts_id = 1
    for day in days:
        for hour in hours:
            timeslots.append(TimeSlot(ts_id, day, hour))
            ts_id += 1
            
    return professors, rooms, courses, timeslots
