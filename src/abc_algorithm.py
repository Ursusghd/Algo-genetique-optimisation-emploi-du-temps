import random
import numpy as np
import copy
from typing import List, Dict
from .models import Schedule, Assignment, Course, Room, TimeSlot

class ArtificialBeeColony:
    def __init__(self, courses, rooms, timeslots, pop_size=50, limit=20):
        self.courses = courses
        self.rooms = rooms
        self.timeslots = timeslots
        self.pop_size = pop_size
        self.limit = limit  # Maximum trials before a food source is abandoned (scout phase)
        
        # Initialize population (food sources)
        self.population = [self.create_random_schedule() for _ in range(self.pop_size)]
        self.fitnesses = [self.calculate_fitness(s) for s in self.population]
        self.trials = [0 for _ in range(self.pop_size)]  # Track trials for scout phase

    def create_random_schedule(self) -> Schedule:
        assignments = {}
        for course in self.courses:
            room = random.choice(self.rooms)
            timeslot = random.choice(self.timeslots)
            assignments[course] = Assignment(course, room, timeslot)
        return Schedule(assignments)

    def calculate_fitness(self, schedule: Schedule) -> float:
        conflicts = 0
        prof_slots = {}
        room_slots = {}
        
        for assignment in schedule.assignments.values():
            # Check room capacity
            if assignment.room.capacity < assignment.course.student_count:
                conflicts += 1
                
            # Check professor scheduling conflicts
            prof_key = (assignment.course.professor.id, assignment.timeslot.id)
            if prof_key in prof_slots:
                conflicts += 1
            else:
                prof_slots[prof_key] = True
                
            # Check room scheduling conflicts
            room_key = (assignment.room.id, assignment.timeslot.id)
            if room_key in room_slots:
                conflicts += 1
            else:
                room_slots[room_key] = True
        
        return 1 / (conflicts + 1)

    def get_neighbor(self, schedule: Schedule) -> Schedule:
        # Clone the schedule
        new_assignments = {}
        for course, assignment in schedule.assignments.items():
            # Copy assignment to avoid modifying the original during search
            new_assignments[course] = Assignment(assignment.course, assignment.room, assignment.timeslot)
            
        new_schedule = Schedule(new_assignments)
        
        # Randomly select a course and mutate its room or timeslot
        course_to_mutate = random.choice(self.courses)
        if random.random() < 0.5:
            new_schedule.assignments[course_to_mutate].room = random.choice(self.rooms)
        else:
            new_schedule.assignments[course_to_mutate].timeslot = random.choice(self.timeslots)
            
        return new_schedule

    def employed_bees_phase(self):
        for i in range(self.pop_size):
            neighbor = self.get_neighbor(self.population[i])
            neighbor_fitness = self.calculate_fitness(neighbor)
            
            if neighbor_fitness > self.fitnesses[i]:
                self.population[i] = neighbor
                self.fitnesses[i] = neighbor_fitness
                self.trials[i] = 0
            else:
                self.trials[i] += 1

    def onlooker_bees_phase(self):
        # Probability based on fitness (roulette wheel selection)
        total_fitness = sum(self.fitnesses)
        if total_fitness == 0:
            probabilities = [1/self.pop_size] * self.pop_size
        else:
            probabilities = [f / total_fitness for f in self.fitnesses]
            
        for _ in range(self.pop_size):
            # Select an index based on probabilities
            i = np.random.choice(range(self.pop_size), p=probabilities)
            
            neighbor = self.get_neighbor(self.population[i])
            neighbor_fitness = self.calculate_fitness(neighbor)
            
            if neighbor_fitness > self.fitnesses[i]:
                self.population[i] = neighbor
                self.fitnesses[i] = neighbor_fitness
                self.trials[i] = 0
            else:
                self.trials[i] += 1

    def scout_bees_phase(self):
        for i in range(self.pop_size):
            if self.trials[i] > self.limit:
                # Abandon food source and find a new one
                self.population[i] = self.create_random_schedule()
                self.fitnesses[i] = self.calculate_fitness(self.population[i])
                self.trials[i] = 0

    def solve(self, max_iterations=100):
        history = []
        best_idx = np.argmax(self.fitnesses)
        best_schedule = self.population[best_idx]
        best_fitness = self.fitnesses[best_idx]
        
        for iteration in range(max_iterations):
            self.employed_bees_phase()
            self.onlooker_bees_phase()
            self.scout_bees_phase()
            
            # Update best
            current_best_idx = np.argmax(self.fitnesses)
            if self.fitnesses[current_best_idx] > best_fitness:
                best_fitness = self.fitnesses[current_best_idx]
                best_schedule = self.population[current_best_idx]
            
            history.append(best_fitness)
            print(f"ABC Iteration {iteration}: Best Fitness = {best_fitness:.4f}, Conflicts = {int(1/best_fitness - 1)}")
            
            if best_fitness == 1.0:
                break
                
        return best_schedule, history
