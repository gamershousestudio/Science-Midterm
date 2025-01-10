class Fitness:
    # Calculates the ranking for each car
    def calculate_cost(car_sprites):
        for car in car_sprites:
            car.network.highest_checkpoint = car.last_checkpoint_passed

class RankChromosomes:
    # Creates chromosomes
    def __init__(self, highest_checkpoint, chromosome):
        self.highest_checkpoint = highest_checkpoint
        self.chromosome = chromosome

    # Rank selection
    def __lt__(self, other):
        return self.highest_checkpoint > other.highest_checkpoint