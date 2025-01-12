class Fitness:
    # Calculates the ranking for each car
    def calculate_cost(car_sprites):
        for car in car_sprites:
            car.network.highest_checkpoint = car.last_checkpoint_passed

class RankChromosomes:
    # Creates chromosomes
    def __init__(self, highest_checkpoint, chromosome): # TODO: add time taken perameter
        self.highest_checkpoint = highest_checkpoint
        self.chromosome = chromosome

        # TODO: store time taken perameter

    # Rank selection
    def __lt__(self, other):
        return self.highest_checkpoint > other.highest_checkpoint
    
    # TODO: least time taken scores the best
    # TODO: check if highest checkpoints are the same(if self.highest_checkpoint == other.highest_checkpoint)
    # TODO: check if the time is faster(return self.time_taken > other.time_taken)
    
    