from azure.quantum import Workspace

# Copy the settings for your workspace below
workspace = Workspace (
    # subscription_id = "",  # Add your subscription_id
    # resource_group = "",   # Add your resource_group
    # name = "",             # Add your workspace name
    # location = ""          # Add your workspace location (for example, "westus")
)
workspace.login()

from typing import List
from azure.quantum.optimization import Problem, ProblemType, Term

def createProblemForContainerWeights(containerWeights: List[int]) -> List[Term]:

    terms: List[Term] = []

    # Expand the squared summation
    for i in range(len(containerWeights)):
        for j in range(len(containerWeights)):
            if i == j:
                # Skip the terms where i == j as they can be disregarded:
                # w_i∗w_j∗x_i∗x_j = w_i*w_j∗(x_i)^2 = w_i∗w_j
                # for x_i = x_j, x_i ∈ {1, -1}
                continue

            terms.append(
                Term(
                    c = containerWeights[i] * containerWeights[j],
                    indices = [i, j]
                )
            )

    return terms

# This array contains a list of the weights of the containers:
containerWeights = [1, 5, 9, 21, 35, 5, 3, 5, 10, 11]

# Create the Terms for this list of containers:
terms = createProblemForContainerWeights(containerWeights)

# Create the Problem to submit to the solver:
problem = Problem(name="Ship Loading Problem", problem_type=ProblemType.ising, terms=terms)

from azure.quantum.optimization import ParallelTempering

# Instantiate a solver instance to solve the problem
solver = ParallelTempering(workspace, timeout=100) # timeout in seconds

# Optimize the problem
result = solver.optimize(problem)

def printResultSummary(result):
    # Print a summary of the result
    shipAWeight = 0
    shipBWeight = 0
    for container in result['configuration']:
        containerAssignment = result['configuration'][container]
        containerWeight = containerWeights[int(container)]
        ship = ''
        if containerAssignment == 1:
            ship = 'A'
            shipAWeight += containerWeight
        else:
            ship = 'B'
            shipBWeight += containerWeight

        print(f'Container {container} with weight {containerWeight} was placed on Ship {ship}')

    print(f'\nTotal weights: \n\tShip A: {shipAWeight} tonnes \n\tShip B: {shipBWeight} tonnes')

printResultSummary(result)