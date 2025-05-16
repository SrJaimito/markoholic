class StateDatabase:

    def __init__(self):
        self.state_to_value = {}
        self.value_to_state = {}


    def add(self, id: str, value: int = None):
        if id in self.state_to_value:
            raise ValueError(f'State "{id}" is already defined')

        if value is not None:
            if value in self.value_to_state:
                raise ValueError(
                    f'Value {value} is already assigned to state'
                    f'"{self.value_to_state[value]}"'
                )

            if value < 0:
                raise ValueError('Value must be possitive')
            
            self.__add(id, value)

        else:
            values = self.value_to_state.keys().sort()

            if values[0] > 0:
                self.__add(id, 0)
                return

            for i in range(len(values) - 1):
                if values[i + 1] > values[i] + 1:
                    self.__add(id, values[i] + 1)
                    return

            self.__add(id, values[-1] + 1)


    def __add(self, id: str, value: int):
        self.state_to_value[id] = value
        self.value_to_state[value] = id


    def get_value_of(self, id: str) -> int:
        if id not in self.state_to_value:
            raise ValueError(f'State "{id}" does not exist')

        return self.state_to_value[id]


    def get_id_of(self, value: int) -> str:
        if value not in self.value_to_state:
            raise ValueError(f'There is no state with value {value}')

        return self.state_to_value[id]


    def get_all_ids(self) -> list[str]:
        return self.state_to_value.keys()


    def get_all_values(self) -> list[int]:
        return self.value_to_state.keys()


    def is_empty(self):
        return len(self.state_to_value) == 0


    def is_valid(self, id: str) -> bool:
        return id in self.state_to_value

