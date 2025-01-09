class Evolution:
    def __init__(self, population_count, keep_count):
        self.population_count = population_count
        self.keep_count = keep_count

    def execute(self, rankable_chromosomes):

        offspring = []

        assert len(offspring) == self.population_count

        return offspring