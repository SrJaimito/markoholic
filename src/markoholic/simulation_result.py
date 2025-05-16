import copy
import numpy as np
import matplotlib.pyplot as plt


class SimulationResult:

    def __init__(self, state_info: StateDatabase):
        self.state_info = state_info
        self.results = []


    def include(self, time: list[float], state: list[int]):
        self.results.append([time.copy(), state.copy()])


    def plot(self, path: str, index: int = -1, title: str = ''):
        if len(self.results) == 0:
            raise Exception('No simulation results available')

        state_ids = self.state_info.get_all_ids()
        state_values = [state_info.get_value_of(id) for id in state_ids]

        fig, ax = plt.figure()

        ax.step(self.results[index][0], self.results[index][1], color = 'black')

        ax.set_xlabel('Time')
        ax.set_ylabel('State')
        ax.set_title(title)
        ax.set_xticks(state_values, state_ids)
        
        fig.savefig(path, bbox_inches = 'tight')

