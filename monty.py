#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Monte-Carlo simulation of the Monty Hall problem for estimating the
probability of the "change doors" strategy.

Copyright 2013 Rogério Theodoro de Brito <rbrito@ime.usp.br>
"""

import random


def init_doors():
    """
    Create a configuration (a list) of 3 doors with 2 goats (represented by
    'g') and 1 car (represented by 'c'), with the car being uniformly
    distributed among the 3 doors.

    Returns a list with the contents of the doors and the position of the
    prize.
    """
    doors = ['g', 'g', 'g']
    prize_pos = random.randint(0, 2)
    doors[prize_pos] = 'c'
    return doors, prize_pos


def first_participant_choice():
    """
    Return the first choice made by the participant of the show, uniformly
    distributed, before Monty shows one of the doors without the car (the
    prize).
    """
    return random.randint(0, 2)


def monty_shows(doors, prize_pos, choice):
    """
    Given a list with the configuration of the 3 doors, the prize position,
    and the choice made by the participant, reveal one of the doors not
    chosen by the participant and that does not contain the prize.
    """
    # FIXME: nasty code, to make it cleaner
    doors_clone = list(doors)
    doors_clone[prize_pos] = 'x'  # kill the prize position
    doors_clone[choice] = 'x'  # kill the participant's choice

    return doors_clone.index('g')


def switch_strategy():
    """
    Performs a trial of the "switch doors strategy".  We return 1 if the
    participant won the prize and 0 otherwise.
    """
    doors, prize_pos = init_doors()

    choice = first_participant_choice()
    pos_shown = monty_shows(doors, prize_pos, choice)

    # The doors chosen by the participant and Monty are distinct and the
    # indices of the doors sum up to 0 + 1 + 2 = 3. So, the participant
    # chooses switches to the position (3 - choice - pos_shown)
    new_choice = 3 - choice - pos_shown

    if doors[new_choice] == 'c':
        return 1
    return 0


def keep_strategy():
    """
    Performs a trial of the "keep doors strategy".  We return 1 if the
    participant won the prize and 0 otherwise.
    """
    doors, prize_pos = init_doors()

    choice = first_participant_choice()
    # The participant simply sticks to his choice, regardless of what Monty
    # shows.

    if doors[choice] == 'c':
        return 1
    return 0


def main():
    """
    The real simulations.
    """
    n = 10000

    successes = 0.0
    for i in range(n):
        successes += switch_strategy()
    print("After %d trials with the switch doors strategy,"
          " the observed frequency of success was %f." % (n, successes/n))

    successes = 0.0
    for i in range(n):
        successes += keep_strategy()
    print("After %d trials with the keep doors strategy,"
          " the observed frequency of success was %f." % (n, successes/n))


if __name__ == '__main__':
    main()
