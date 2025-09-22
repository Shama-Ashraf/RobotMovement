import numpy as np
import pygad
import matplotlib.pyplot as plt

# Define grid size and obstacles
GRID_SIZE = 20
OBSTACLES = {(5, 5), (5, 6), (5, 7), (10, 10), (11, 10), (12, 10), (15, 15), (15, 14)}

START = (0, 0)
GOAL = (19, 19)
NUM_WAYPOINTS = 10

# Gene space definition: x and y between 0 and GRID_SIZE-1
gene_space = [{'low': 0, 'high': GRID_SIZE - 1} for _ in range(NUM_WAYPOINTS * 2)]

# Helper functions
def path_length(path):
    dist = 0
    for i in range(len(path) - 1):
        dist += np.linalg.norm(np.array(path[i+1]) - np.array(path[i]))
    return dist

def has_collision(point):
    return tuple(map(int, point)) in OBSTACLES

def decode_solution(solution):
    path = [START]
    for i in range(0, len(solution), 2):
        x = int(np.clip(solution[i], 0, GRID_SIZE - 1))
        y = int(np.clip(solution[i+1], 0, GRID_SIZE - 1))
        path.append((x, y))
    path.append(GOAL)
    return path

# Fitness function
def fitness_func(ga_instance, solution, solution_idx):
    path = decode_solution(solution)
    collisions = sum(has_collision(p) for p in path)
    length = path_length(path)
    fitness = -1 * (length + 10 * collisions)
    return fitness

# GA setup
ga_instance = pygad.GA(
    num_generations=100,
    num_parents_mating=10,
    fitness_func=fitness_func,
    sol_per_pop=50,
    num_genes=NUM_WAYPOINTS * 2,
    gene_space=gene_space,
    mutation_percent_genes=10,
    crossover_type="two_points",
    parent_selection_type="tournament",
    mutation_type="random"
)

# Run GA
ga_instance.run()

# Best solution
solution, solution_fitness, _ = ga_instance.best_solution()
path = decode_solution(solution)

print("Best Path:", path)
print("Path Length:", path_length(path))

# Plot final path
plt.figure(figsize=(8, 8))
plt.grid(True)
plt.xlim(0, GRID_SIZE)
plt.ylim(0, GRID_SIZE)
plt.title("Optimal Path Found by Genetic Algorithm")
plt.plot(*zip(*path), marker='o', label='Path')
for obs in OBSTACLES:
    plt.plot(obs[0], obs[1], 'ks', markersize=15)  # obstacle in black
plt.plot(START[0], START[1], 'go', markersize=10, label='Start')
plt.plot(GOAL[0], GOAL[1], 'ro', markersize=10, label='Goal')
plt.legend()
plt.show()

# Plot fitness over generations
ga_instance.plot_fitness(title="GA Fitness Convergence")
