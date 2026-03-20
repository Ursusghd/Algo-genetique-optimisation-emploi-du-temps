from src.data_loader import generate_sample_data
from src.genetic_algorithm import GeneticAlgorithm
from src.abc_algorithm import ArtificialBeeColony
from src.visualization import plot_fitness_history, display_schedule

def main():
    print("Initialisation de l'optimisation d'emploi du temps...")
    
    # 1. Charger les données
    profs, rooms, courses, timeslots = generate_sample_data()
    
    # Choix de l'algorithme
    ALGO_CHOICE = "ABC"  # Changez en "GA" ou "ABC"


    
    if ALGO_CHOICE == "GA":
        print("\n--- Utilisation de l'Algorithme Génétique ---")
        ga = GeneticAlgorithm(
            courses=courses,
            rooms=rooms,
            timeslots=timeslots,
            pop_size=50,
            mutation_rate=0.1
        )
        best_schedule, history = ga.evolve(generations=100)
    else:
        print("\n--- Utilisation de la Colonie d'Abeilles (ABC) ---")
        abc = ArtificialBeeColony(
            courses=courses,
            rooms=rooms,
            timeslots=timeslots,
            pop_size=50,
            limit=20
        )
        best_schedule, history = abc.solve(max_iterations=100)
    
    # 4. Afficher les résultats
    plot_fitness_history(history)
    display_schedule(best_schedule)
    
    # Recalculer la fitness finale pour l'affichage
    if ALGO_CHOICE == "GA":
        final_fitness = ga.calculate_fitness(best_schedule)
    else:
        final_fitness = abc.calculate_fitness(best_schedule)

    if final_fitness == 1.0:
        print("\nSuccès : Un emploi du temps sans conflit a été trouvé !")
    else:
        conflicts = int(1/final_fitness - 1)
        print(f"\nTerminé : L'emploi du temps contient encore {conflicts} conflit(s).")

if __name__ == "__main__":
    main()

