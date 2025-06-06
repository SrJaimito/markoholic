import copy

import numpy as np
import scipy.interpolate as interp
import matplotlib.pyplot as plt

from markoholic.chains.state_set import StateSet


class SimulationResult:

    def __init__(self, state_info: StateSet):
        self.state_info = state_info
        self.results = {
            'evolutions': [],
            'failure_times': []
        }


    def include(self, time: list[float], state: list[int], failure_time: float):
        if len(self.results['evolutions']) != 0:
            ref_time_start = self.results['evolutions'][0]['time'][0]
            ref_time_end = self.results['evolutions'][0]['time'][-1]

            if time[0] != ref_time_start or time[-1] != ref_time_end:
                raise ValueError('New results are not compatible with previous ones')

        self.results['evolutions'].append({
            'time': time.copy(),
            'state': state.copy()
        })

        if failure_time is not None:
            self.results['failure_times'].append(failure_time)


    def plot_state(self, index: int = -1, **kwargs):
        if len(self.results['evolutions']) == 0:
            raise Exception('No simulation results available')

        state_ids = self.state_info.get_all_ids()
        state_values = [self.state_info.get_value_of(id) for id in state_ids]

        fig = plt.figure()

        plt.step(
            self.results['evolutions'][index]['time'],
            self.results['evolutions'][index]['state'],
            where = 'post'
        )

        plt.xlabel('Time')
        plt.ylabel('State')
        plt.yticks(state_values, state_ids)

        if 'title' in kwargs:
            plt.title(kwargs['title'])
        
        if 'save_path' in kwargs:
            fig.savefig(kwargs['save_path'], bbox_inches = 'tight')
        else:
            plt.show()


    def plot_probabilities(self, steps: int = 1000, **kwargs):
        encoding = self.__one_hot_encoding()

        time_start = self.results['evolutions'][0]['time'][0]
        time_end = self.results['evolutions'][0]['time'][-1]

        time_grid = np.linspace(time_start, time_end, steps + 1)
        states = []

        for result in self.results['evolutions']:
            interpolator = interp.interp1d(
                result['time'], result['state'],
                kind = 'previous',
                bounds_error = False,
                fill_value = (result['state'][0], result['state'][-1])
            )
            
            interp_states = interpolator(time_grid)
            interp_states = [encoding[s] for s in interp_states]

            states.append(interp_states)

        states = np.array(states)

        probabilities = np.sum(states, axis = 0) / len(self.results['evolutions'])

        fig = plt.figure()

        defined_states = sorted(self.state_info.get_all_values())
        for i in range(len(defined_states)):
            label = self.state_info.get_id_of(defined_states[i])
            line, = plt.plot(time_grid, probabilities[:, i], label = label)

        plt.ylabel('Probability')
        plt.legend()

        if 'time_units' in kwargs:
            time_units = kwargs['time_units']
            plt.xlabel(f'Time ({time_units})')
        else:
            plt.xlabel('Time')

        if 'title' in kwargs:
            plt.title(kwargs['title'])
        
        if 'save_path' in kwargs:
            fig.savefig(kwargs['save_path'], bbox_inches = 'tight')
        else:
            plt.show()


    def plot_failure_times(self, **kwargs):
        if len(self.results['failure_times']) == 0:
            raise Exception('This model never failed. Does it have absorving states?')

        mean_failure_time = np.mean(self.results['failure_times'])

        plt.figure()

        plt.hist(self.results['failure_times'], bins = 50, edgecolor = 'black')

        plt.vlines(mean_failure_time, 0, plt.gca().get_ylim()[1],
                        color = 'red', linestyles = 'dashed', label = 'MTTF')

        plt.ylabel('Number of samples')
        plt.legend()

        if 'time_units' in kwargs:
            time_units = kwargs['time_units']
            plt.xlabel(f'Time ({time_units})')
        else:
            plt.xlabel('Time')

        if 'title' in kwargs:
            plt.title(kwargs['title'])
        
        if 'save_path' in kwargs:
            fig.savefig(kwargs['save_path'], bbox_inches = 'tight')
        else:
            plt.show()


    def __one_hot_encoding(self):
        states = sorted(self.state_info.get_all_values())
        n = len(states)

        encoding = {}
        for i in range(n):
            v = [0] * n
            v[i] = 1

            encoding[states[i]] = v

        return encoding

