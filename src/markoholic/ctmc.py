from .state_set import StateSet
from .transition_set import TransitionSet
from .simulation_result import SimulationResult

import numpy.random as rng


class CTMC:

    def __init__(self):
        self.states = StateSet()
        self.transitions = None


    def add_state(self, id: str, value: int = None):
        self.states.add(id, value)


    def define_transition(self, origin: str, destiny: str, rate: float):
        if self.transitions is None:
            if self.states.is_empty():
                return Exception('No states defined')

            self.transitions = TransitionSet(self.states)

        self.transitions.add(origin, destiny, rate)


    def modify_transition(self, origin: str, destiny: str, rate: float):
        if self.transitions is None:
            raise Exception('There are no transitions defined')

        self.transitions.modify(origin, destiny, rate)


    def simulate(self, initial_state: str, time_interval: tuple[float, float], iterations: int = 1) -> SimulationResult:
        if not self.states.is_valid(initial_state):
            raise ValueError('Initial state does not exist')

        time_start, time_end = time_interval

        if time_start >= time_end:
            raise ValueError('Time interval is not increasing')
        
        if iterations <= 0:
            raise ValueError('Number of iterations must be possitive')

        result = SimulationResult(self.states)
        initial_state_value = self.states.get_value_of(initial_state)

        for _ in range(iterations):
            current_time = time_start
            current_state = initial_state_value

            time = []
            state = []

            while current_time < time_end:
                time.append(current_time)
                state.append(current_state)

                available_transitions = self.transitions.get_transitions_from(current_state)

                if len(available_transitions) == 0:
                    break

                transition_times = []

                for transition in available_transitions:
                    rate = transition[1]
                    transition_time = rng.exponential(1 / rate)

                    transition_times.append(transition_time)

                delta_time = min(transition_times)
                delta_time_index = transition_times.index(delta_time)

                current_time += delta_time
                current_state = available_transitions[delta_time_index][0]

            time.append(time_end)
            state.append(state[-1])

            result.include(time, state)

        return result

