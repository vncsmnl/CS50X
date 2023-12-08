# Simulate a sports tournament

import csv
import sys
import random

# Number of simulations to run
N = 10000


def main():
    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = read_teams_from_file(sys.argv[1])

    counts = simulate_tournaments(teams)

    print_team_chances(counts)


def read_teams_from_file(filename):
    """Read teams into memory from file."""
    teams = []
    with open(filename) as file:
        reader = csv.DictReader(file)
        for team in reader:
            team["rating"] = int(team["rating"])
            teams.append(team)
    return teams


def simulate_tournaments(teams):
    """Simulate N tournaments and keep track of win counts."""
    counts = {}
    for i in range(N):
        winner = simulate_tournament(teams)
        counts[winner] = counts.get(winner, 0) + 1
    return counts


def print_team_chances(counts):
    """Print each team's chances of winning, according to simulation."""
    for team in sorted(counts, key=lambda t: counts[t], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1, rating2 = team1["rating"], team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    return [
        teams[i] if simulate_game(teams[i], teams[i + 1]) else teams[i + 1]
        for i in range(0, len(teams), 2)
    ]


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    while len(teams) > 1:
        teams = simulate_round(teams)
    return teams[0]["team"]


if __name__ == "__main__":
    main()
