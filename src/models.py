from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class Professor:
    id: int
    name: str

@dataclass(frozen=True)
class Room:
    id: int
    name: str
    capacity: int

@dataclass(frozen=True)
class Course:
    id: int
    name: str
    professor: Professor
    student_count: int

@dataclass(frozen=True)
class TimeSlot:
    id: int
    day: str
    hour: str

@dataclass
class Schedule:
    assignments: Dict[Course, 'Assignment']

@dataclass
class Assignment:
    course: Course
    room: Room
    timeslot: TimeSlot
