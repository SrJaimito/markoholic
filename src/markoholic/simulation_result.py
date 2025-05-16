import copy

import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt


class SimulationResult:

    def __init__(self, state_info: StateDatabase):
        self.state_info = state_info
        self.results = []


    def include(self, time: list[float], state: list[int]):
        if len(self.results) != 0:
            ref_time_start = self.results[0][0][0]
            ref_time_end = self.results[0][0][-1]

            if time[0] != ref_time_start or time[-1] != ref_time_end:
                raise ValueError('New results are not compatible with previous ones')

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


    def plot_probabilities(self, path: str, num_points: int = 1000):
        pass

