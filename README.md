# Optimisation d'Emploi du Temps Universitaire par Algorithme Génétique

Ce projet utilise un algorithme génétique pour résoudre le problème complexe de la planification des cours universitaires. L'objectif est de minimiser les conflits (professeurs, salles, capacités) et d'automatiser la génération d'un emploi du temps optimal.

## Fonctionnalités

- **Algorithme Génétique robuste** : Gère la sélection par tournoi, le croisement en un point et la mutation aléatoire.
- **Algorithme de Colonie d'Abeilles (ABC)** : Comprend les phases des abeilles employées, spectatrices et éclaireuses pour une recherche globale efficace.
- **Gestion des contraintes** : 
    - Un professeur ne peut pas être à deux endroits à la fois.
    - Une salle ne peut pas accueillir deux cours simultanément.
    - La capacité de la salle doit être respectée.
- **Visualisation** : Génération automatique d'un graphique d'évolution de la fitness.
- **Export Tabulaire** : Affichage clair de l'emploi du temps final via Pandas.

## Structure du Projet

```text
├── src/
│   ├── models.py           # Définition des classes (Professor, Room, Course, etc.)
│   ├── data_loader.py      # Génération/Chargement des données de test
│   ├── genetic_algorithm.py # Moteur de l'algorithme génétique
│   ├── abc_algorithm.py    # Moteur de l'algorithme de colonie d'abeilles
│   └── visualization.py    # Outils d'affichage et graphiques
├── main.py                 # Point d'entrée principal (choix de l'algorithme disponible)
└── README.md               # Documentation
```


## Installation

```bash
pip install numpy pandas matplotlib
```

## Utilisation

Pour lancer l'optimisation :

```bash
python main.py
```

Les résultats seront affichés dans la console et un graphique `fitness_evolution.png` sera généré.

## Paramètres de l'Algorithme

Vous pouvez ajuster les paramètres dans `main.py` :
- `pop_size` : Taille de la population.
- `mutation_rate` : Probabilité de mutation par gène.
- `generations` : Nombre maximum d'itérations.
