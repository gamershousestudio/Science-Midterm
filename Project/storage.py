import json

# Stores chromosomes
class Storage:
    def __init__(self, filename):
        self.filename = filename
    
    # Saves to json file
    def save(self, chromosomes):
        with open(self.filename, "w") as file:
            json.dump({"chromosomes": chromosomes}, file)
    
    # Loads to the car network
    def load(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                return data["chromosomes"]
        except Exception:
            return []