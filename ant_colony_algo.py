import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import time

class AntColonyOptimization:
    def __init__(self, numAnts=20, maxIterations=100, alpha=1, beta=2, rho=0.8):
        self.graph = None  # The graph to be colored
        self.numAnts = numAnts  # Number of ants in the colony
        self.maxIterations = maxIterations  # Maximum iterations for the algorithm
        self.alpha = alpha  # Influence of pheromone on decision-making
        self.beta = beta  # Influence of heuristic information on decision-making
        self.rho = rho  # Pheromone evaporation rate
        self.numNodes = None  # Number of nodes in the graph
        self.pheromoneMatrix = None  # Pheromone matrix
        self.bestSolution = None  # Best solution found
        self.bestFitness = float('inf')  # Best fitness value found
        self.fitnessHistory = []  # History of best fitness values over iterations
        self.avgFitnessHistory = []  # History of average fitness values over iterations

    def loadGraph(self, filename):
        # Load graph from file
        graph = {}
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('e'):
                    _, node1, node2 = line.split()
                    node1, node2 = int(node1), int(node2)
                    if node1 not in graph:
                        graph[node1] = []
                    if node2 not in graph:
                        graph[node2] = []
                    graph[node1].append(node2)
                    graph[node2].append(node1)
        return graph

    def calculateFitness(self, ant):
        # Calculate fitness of an ant's coloring solution
        return len(set(ant.coloring.values()))

    def selectNextNode(self, ant, unvisited):
        # Select next node to visit based on pheromone trails and heuristic information
        if not unvisited:
            return None
        nodeProbabilities = {}
        for node in unvisited:
            pheromoneValue = self.pheromoneMatrix[ant.currentNode - 1][node - 1]
            desirability = len(set([ant.coloring[neighbor] for neighbor in self.graph[node] if neighbor in ant.coloring]))
            nodeProbabilities[node] = pheromoneValue ** self.alpha * desirability ** self.beta
        totalProbability = sum(nodeProbabilities.values())
        if totalProbability == 0:
            return random.choice(unvisited)
        normalizedProbabilities = {node: prob / totalProbability for node, prob in nodeProbabilities.items()}
        return np.random.choice(list(normalizedProbabilities.keys()), p=list(normalizedProbabilities.values()))

    def runAlgorithm(self, filename):
        # Run the Ant Colony Optimization algorithm
        self.graph = self.loadGraph(filename)
        self.numNodes = len(self.graph)
        maxNodeIndex = max(self.graph.keys())
        self.pheromoneMatrix = np.ones((maxNodeIndex, maxNodeIndex)) * 0.01
        for iteration in range(self.maxIterations):
            ants = [Ant(self.graph) for _ in range(self.numAnts)]
            iterationFitness = []
            for ant in ants:
                ant.startTour()
                while not ant.tourComplete:
                    nextNode = self.selectNextNode(ant, ant.unvisited)
                    if nextNode is None:
                        break
                    ant.visitNode(nextNode)
            for ant in ants:
                fitness = self.calculateFitness(ant)
                iterationFitness.append(fitness)
                if fitness < self.bestFitness:
                    self.bestFitness = fitness
                    self.bestSolution = ant.coloring.copy()
                ant.updatePheromone(self.pheromoneMatrix, self.rho)
            avgFitness = np.mean(iterationFitness)
            self.avgFitnessHistory.append(avgFitness)
            self.fitnessHistory.append(self.bestFitness)
            if(iteration % 10 == 0):
                print(f"Iteration {iteration}: Best fitness {self.bestFitness}, Average fitness {avgFitness}")
        print(f"Best fitness: {self.bestFitness} AND Average fitness: {avgFitness} after {self.maxIterations} iterations.")
        self.performLocalSearch()
        self.visualizeSolution()

    def performLocalSearch(self):
        # Perform local search to improve the best solution found
        currentSolution = self.bestSolution.copy()
        improved = True
        while improved:
            improved = False
            for node in self.graph:
                neighbors = self.graph[node]
                _ = currentSolution[node]
                neighborColors = [currentSolution[neighbor] for neighbor in neighbors]
                availableColors = set(range(1, self.bestFitness + 1)) - set(neighborColors)
                for color in availableColors:
                    newSolution = currentSolution.copy()
                    newSolution[node] = color
                    newFitness = len(set(newSolution.values()))
                    if newFitness < self.bestFitness:
                        currentSolution = newSolution
                        self.bestSolution = newSolution
                        self.bestFitness = newFitness
                        improved = True
                        break

    def visualizeSolution(self):
        # Visualize the best solution found
        G = nx.Graph()
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        colors = [self.bestSolution[node] for node in G.nodes()]
        pos = nx.spring_layout(G)
        plt.figure(figsize=(20, 12))
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, cmap=plt.cm.viridis, font_color='white', edge_color='gray', width=0.5)
        plt.title('Graph Coloring using Ant Colony Optimization')
        plt.show()

class Ant:
    def __init__(self, graph):
        # Initialize ant with graph information
        self.graph = graph
        self.startNode = None
        self.currentNode = None
        self.unvisited = []
        self.coloring = {}
        self.tourComplete = False

    def startTour(self):
        # Start a new tour
        self.startNode = random.choice(list(self.graph.keys()))
        self.currentNode = self.startNode
        self.unvisited = list(self.graph.keys())
        self.coloring = {node: None for node in self.graph}
        self.unvisited.remove(self.startNode)
        self.tourComplete = False
        self.coloring[self.startNode] = 1

    def visitNode(self, node):
        # Visit a node during the tour
        self.currentNode = node
        self.unvisited.remove(node)
        availableColors = set(range(1, len(self.graph) + 1)) - set(self.coloring[neighbor] for neighbor in self.graph[node] if self.coloring[neighbor] is not None)
        self.coloring[node] = min(availableColors) if availableColors else max(self.coloring.values()) + 1
        if not self.unvisited:
            self.tourComplete = True

    def updatePheromone(self, pheromoneMatrix, rho):
        # Update pheromone levels based on ant's tour
        for node in self.coloring:
            for neighbor in self.graph[node]:
                if self.coloring[node] != self.coloring[neighbor]:
                    pheromoneMatrix[node - 1][neighbor - 1] = (1 - rho) * pheromoneMatrix[node - 1][neighbor - 1] + rho
def main():
    filename = "smaller_data.col"
    start_time = time.time()
    antColonyOptimization = AntColonyOptimization()
    antColonyOptimization.runAlgorithm(filename)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
if __name__ == "__main__":
    main()