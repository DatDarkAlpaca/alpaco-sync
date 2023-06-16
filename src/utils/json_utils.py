import json


class JsonDB:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self.data = self.__initialize_data()

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: str):
        self._filepath = filepath
        self.data = self.__initialize_data()

    def __initialize_data(self) -> dict:
        with open(self.filepath, mode='r', encoding='utf-8') as file:
            return json.load(file)

    def save(self, **kwargs):
        with open(self.filepath, mode='r+', encoding='utf-8') as file:
            json.dump(self.data, file, **kwargs)

    def update_entry(self, entry, value):
        new_object = {
            entry: value
        }
        self.data.update(new_object)

    def remove_entry(self, entry):
        del self.data[entry]
