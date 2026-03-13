import matplotlib.pyplot as plt
import pandas as pd
from .models import Schedule

def plot_fitness_history(history):
    plt.figure(figsize=(10, 6))
    plt.plot(history, marker='o', linestyle='-', color='b')
    plt.title("Évolution de la Fitness au fil des Générations")
    plt.xlabel("Génération")
    plt.ylabel("Fitness (Maximisée à 1.0)")
    plt.grid(True)
    plt.savefig("fitness_evolution.png")
    print("Graphique de fitness sauvegardé sous 'fitness_evolution.png'")

def display_schedule(schedule: Schedule):
    data = []
    for course, assignment in schedule.assignments.items():
        data.append({
            "Cours": course.name,
            "Professeur": course.professor.name,
            "Étudiants": course.student_count,
            "Salle": assignment.room.name,
            "Capacité Salle": assignment.room.capacity,
            "Jour": assignment.timeslot.day,
            "Heure": assignment.timeslot.hour
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values(by=["Jour", "Heure"])
    print("\n--- Emploi du Temps Optimisé ---\n")
    print(df.to_string(index=False))
    return df
