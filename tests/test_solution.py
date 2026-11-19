import numpy as np
import vrplib

from cvrp.solution import solution_cost, is_feasible

def test_reference_solution_cost():
    # 1. Instanz und Referenzlösung einlesen
    instance = vrplib.read_instance("data/A-n32-k5.vrp")
    solution = vrplib.read_solution("data/A-n32-k5.sol")

    # 2. Distanzmatrix korrekt runden
    dist = np.rint(instance["edge_weight"]).astype(int)

    # 3. Gesamtkosten selbst berechnen
    calculated_cost = solution_cost(solution["routes"], dist)

    # 4. Ergebnis überprüfen
    assert calculated_cost == solution["cost"]

def test_missing_customer():
    instance = vrplib.read_instance("data/A-n32-k5.vrp")
    solution = vrplib.read_solution("data/A-n32-k5.sol")

    routes = [r.copy() for r in solution["routes"]]
    routes[0].pop()

    assert is_feasible(
        routes,
        instance["demand"],
        instance["capacity"]
    ) == False

def test_capacity_violation():
    instance = vrplib.read_instance("data/A-n32-k5.vrp")
    solution = vrplib.read_solution("data/A-n32-k5.sol")

    routes = [r.copy() for r in solution["routes"]]
    assert is_feasible(
        routes,
        instance["demand"],
        1
    ) == False

def test_empty_route():
    instance = vrplib.read_instance("data/A-n32-k5.vrp")
    solution = vrplib.read_solution("data/A-n32-k5.sol")

    routes = [r.copy() for r in solution["routes"]]
    routes.append([])

    assert is_feasible(
        routes,
        instance["demand"],
        instance["capacity"]
    ) == False

def test_capacity_boundary():
    instance = vrplib.read_instance("data/A-n32-k5.vrp")
    solution = vrplib.read_solution("data/A-n32-k5.sol")
    routes = [r.copy() for r in solution["routes"]]

    # Prüfe Q = 96
    assert is_feasible(
            routes,
            instance["demand"],
            96
        ) == True

    # Prüfe Q = 95
    assert is_feasible(
            routes,
            instance["demand"],
            95
        ) == False

def test_reference_solution_feasible():
    instance = vrplib.read_instance("data/A-n32-k5.vrp")
    solution = vrplib.read_solution("data/A-n32-k5.sol")

    # Prüfe die Zulässigkeit der Referenzlösung
    assert is_feasible(
        solution["routes"],
        instance["demand"],
        instance["capacity"]
    ) == True

def test_duplicate_customer():
    instance = vrplib.read_instance("data/A-n32-k5.vrp")
    solution = vrplib.read_solution("data/A-n32-k5.sol")

    routes = [r.copy() for r in solution["routes"]]

    # Einen bereits besuchten Kunden erneut einfügen
    routes[2].append(routes[2][1])

    # Mit assert die Unzulässigkeit überprüfen
    assert is_feasible(
        routes,
        instance["demand"],
        instance["capacity"]
    ) is False

def test_invalid_customer_index():
    instance = vrplib.read_instance("data/A-n32-k5.vrp")
    solution = vrplib.read_solution("data/A-n32-k5.sol")

    routes = [r.copy() for r in solution["routes"]]
    routes[0].append(32)

    assert is_feasible(
        routes,
        instance["demand"],
        instance["capacity"]
    ) is False

def test_empty_solution():
    instance = vrplib.read_instance("data/A-n32-k5.vrp")

    # Prüfe eine Lösung ohne Touren
    assert is_feasible(
        [],
        instance["demand"],
        instance["capacity"]
    ) is False