import random
from typing import List, Dict
import numpy as np
from .models import Schedule, Assignment, Course, Room, TimeSlot

class GeneticAlgorithm:
    def __init__(self, courses, rooms, timeslots, pop_size=100, mutation_rate=0.1, crossover_rate=0.8):
        self.courses = courses
        self.rooms = rooms
        self.timeslots = timeslots
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

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
        
        # Fitness is inversely proportional to conflicts
        # Adding 1 to avoid division by zero
        return 1 / (conflicts + 1)

    def select(self, population: List[Schedule], fitnesses: List[float]) -> Schedule:
        # Tournament selection
        tournament_size = 3
        best_ind = random.randint(0, len(population) - 1)
        
        for _ in range(tournament_size - 1):
            ind = random.randint(0, len(population) - 1)
            if fitnesses[ind] > fitnesses[best_ind]:
                best_ind = ind
        return population[best_ind]


    def crossover(self, parent1: Schedule, parent2: Schedule) -> Schedule:
        if random.random() > self.crossover_rate:
            return parent1
            
        child_assignments = {}
        # Single point crossover on the dictionary of assignments
        split_point = random.randint(0, len(self.courses))
        
        for i, course in enumerate(self.courses):
            if i < split_point:
                child_assignments[course] = parent1.assignments[course]
            else:
                child_assignments[course] = parent2.assignments[course]
                
        return Schedule(child_assignments)

    def mutate(self, schedule: Schedule):
        for course in self.courses:
            if random.random() < self.mutation_rate:
                # Mutate room or timeslot
                if random.random() < 0.5:
                    schedule.assignments[course].room = random.choice(self.rooms)
                else:
                    schedule.assignments[course].timeslot = random.choice(self.timeslots)

    def evolve(self, generations=100):
        population = [self.create_random_schedule() for _ in range(self.pop_size)]
        history = []
        
        for gen in range(generations):
            fitnesses = [self.calculate_fitness(s) for s in population]
            best_fitness = max(fitnesses)
            avg_fitness = sum(fitnesses) / len(fitnesses)
            history.append(best_fitness)
            
            print(f"Generation {gen}: Best Fitness = {best_fitness:.4f}, Conflicts = {int(1/best_fitness - 1)}")
            
            if best_fitness == 1.0: # Optimal found
                break
                
            new_population = []
            # Keep elite
            new_population.append(population[np.argmax(fitnesses)])
            
            while len(new_population) < self.pop_size:
                p1 = self.select(population, fitnesses)
                p2 = self.select(population, fitnesses)
                child = self.crossover(p1, p2)
                self.mutate(child)
                new_population.append(child)
                
            population = new_population
            
        best_schedule = population[np.argmax([self.calculate_fitness(s) for s in population])]
        return best_schedule, history
