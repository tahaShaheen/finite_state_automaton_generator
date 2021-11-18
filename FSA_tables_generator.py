import itertools
from itertools import permutations
import pandas as pd

NO_OF_STATES = 3
ALPHABET = ["a", "b"]
# ALPHABET = ["a", "b", "c"]

POSITIVE_EXAMPLES = ["a", "ab", "baa"]
NEGATIVE_EXAMPLES = ["b", "bb", "ba", "aa", "aba"]

# POSITIVE_EXAMPLES = ["abb"]
# NEGATIVE_EXAMPLES = ["aba"]

# Generate states based on number of states required


def generate_states():
    print("No of states is", NO_OF_STATES)
    states = ["q_"+str(state) for state in range(NO_OF_STATES)]
    return states

# Generate permutations of one accepted and the rest rejected states


def generate_accepted():
    accepted = permutations(
        [" " for i in range(NO_OF_STATES - 1)] + ["V"], NO_OF_STATES)
    accepted = list(dict.fromkeys(accepted))  # removing duplicates
    # for i in accepted:
    #     print(i)
    return accepted


def divide_chunks(l, n):

    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def generate_FSA():
    states = generate_states()
    # print(states)
    accepted = generate_accepted()
    all_combinations = []

    for accept in accepted:
        accept = list(accept)
        states_copy = states.copy()

        combination = []
        for i in range(NO_OF_STATES):
            # combination.append(
            #     [[states_copy.pop(0)], [accept.pop(0)], states, states]
            # )
            combination = combination + \
                [[states_copy.pop(0)]] + [[accept.pop(0)]] + \
                [states for i in range(len(ALPHABET))]
            # [states] + [states]

        all_combinations.append(combination)

    # print(all_combinations)
    print(len(all_combinations), "rows in each table")

    all_FSA = []
    for combination in all_combinations:
        all_FSA = all_FSA + list(itertools.product(*combination))

    print(len(all_FSA), "unique finite state automaton")

    return all_FSA, states


def check_if_accepted(individual_FSA, state_index):
    if individual_FSA[state_index * (2 + len(ALPHABET)) + 1] == "V":
        return True
    else:
        return False


def check_against_examples(all_FSA, states):

    successful_FSA = []
    rejected_FSA = []

    # Checking against POSITIVE EXAMPLES
    for individual_FSA in all_FSA:
        accepted_positive_examples = 0
        for example in POSITIVE_EXAMPLES:
            # print(individual_FSA)
            # print(example)

            state_index = 0

            # splitting the string into list of characters
            for character in list(example):

                # matching with alphabet to find what alphabet this is
                alphabet_index = ALPHABET.index(character)

                # returns the next state
                next_state = individual_FSA[state_index *
                                            (2 + len(ALPHABET)) + alphabet_index + 2]

                # Match with state available
                state_index = states.index(next_state)

                # Go onto next character

            if not check_if_accepted(individual_FSA, state_index):
                # no point in checking the rest of the positive examples if this one was not accepted
                break
            else:
                accepted_positive_examples = accepted_positive_examples + 1

        # record if an FSA accpets all positive examples
        if accepted_positive_examples == len(POSITIVE_EXAMPLES):
            successful_FSA.append(individual_FSA)

    print(len(successful_FSA), "FSA have successfully accepted all positive examples")

    # Checking only the successful FSA against NEGATIVE EXAMPLES

    for individual_FSA in successful_FSA:
        for example in NEGATIVE_EXAMPLES:
            # print(individual_FSA)
            # print(example)

            state_index = 0

            # splitting the string into list of characters
            for character in list(example):

                # matching with alphabet to find what alphabet this is
                alphabet_index = ALPHABET.index(character)

                # returns the next state
                next_state = individual_FSA[state_index *
                                            (2 + len(ALPHABET)) + alphabet_index + 2]

                # Match with state available
                state_index = states.index(next_state)

                # Go onto next character

            if check_if_accepted(individual_FSA, state_index):
                # no point in checking the rest of the negative examples if this one was accepted
                # Also adding the FSA to a list to remove later from the list of successful FSA
                rejected_FSA.append(individual_FSA)
                break

    successful_FSA = [fsa for fsa in successful_FSA if fsa not in rejected_FSA]
    # printing the successful FSA
    if(len(successful_FSA) == 0):
        print("no FSA with", len(states), "states can satisty all the examples")
        print("please try with more states")
    else:
        print(len(successful_FSA), "of those have rejected all negative examples")
        print(successful_FSA)


def main():
    all_FSA, states = generate_FSA()
    check_against_examples(all_FSA, states)


if __name__ == "__main__":
    main()
