import copy

from markoholic.chains.state_set import StateSet


class TransitionSet:

    def __init__(self, state_info: StateSet):
        self.state_info = state_info

        if self.state_info.is_empty():
            raise ValueError('List of states is empty')

        self.transitions = {}
        for state in self.state_info.get_all_values():
            self.transitions[state] = []


    def add(self, origin: str, destination: str, rate: float):
        if not self.state_info.is_valid(origin):
            raise ValueError(f'State "{origin}" is not defined')

        if not self.state_info.is_valid(destination):
            raise ValueError(f'State "{destination}" is not defined')

        if origin == destination:
            raise ValueError('Self loops are not allowed')

        origin_value = self.state_info.get_value_of(origin)
        destination_value = self.state_info.get_value_of(destination)

        defined_transitions = [t[0] for t in self.transitions[origin_value]]

        if destination_value in defined_transitions:
            raise ValueError(
                f'Transition from "{origin}" to "{destination}" is already defined'
            )

        self.transitions[origin_value].append([destination_value, rate])


    def modify(self, origin: str, destination: str, rate: float):
        if not self.state_info.is_valid(origin):
            raise ValueError(f'State "{origin}" is not defined')

        if not self.state_info.is_valid(destination):
            raise ValueError(f'State "{origin}" is not defined')

        origin_value = self.state_info.get_value_of(origin)
        destination_value = self.state_info.get_value_of(destination)

        defined_transitions = [t[0] for t in self.transitions[origin_value]]

        if destination_value not in defined_transitions:
            raise ValueError(
                f'Transition from "{origin}" to "{destination}" is not defined'
            )

        for i in range(len(self.transitions[origin_value])):
            if self.transitions[origin_value][i][0] == destination_value:
                self.transitions[origin_value][i] = [destination_value, rate]


    def get_transitions_from(self, origin: int) -> list[list[int, float]]:
        return copy.deepcopy(self.transitions[origin])

