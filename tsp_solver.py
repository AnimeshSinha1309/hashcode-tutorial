"""Simple travelling salesman problem between cities."""
import collections

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import utils

file = "b_lovely_landscapes"


def create_data_model():
    """Stores the data for the problem."""
    alignments, tags = utils.read_input(file)
    find_tag = collections.defaultdict(list)
    for idx, image_tags in enumerate(tags):
        for tag in image_tags:
            find_tag[tag].append(idx)
    pairs = set()
    for key, value in find_tag.items():
        if len(value) == 2:
            if value[0] > value[1]:
                value[1], value[0] = value[0], value[1]
            pairs.add((value[0], value[1]))
        elif len(value) > 2:
            raise ValueError("The same tag appears in %d photos, not expected in subpart-B" % len(value))
    return pairs, len(tags)


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    edges, n_nodes = create_data_model()
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(n_nodes + 1, 1, n_nodes)
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        if from_node > to_node:
            from_node, to_node = to_node, from_node
        if to_node == n_nodes:
            return 0
        return 0 if (from_node, to_node) in edges else 1000000

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()

    search_parameters.time_limit.seconds = 1
    search_parameters.solution_limit = 1
    search_parameters.lns_time_limit.seconds = 1

    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # Solve the problem.
    print("Starting Solver")
    solution = routing.SolveWithParameters(search_parameters)
    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)


if __name__ == '__main__':
    main()
