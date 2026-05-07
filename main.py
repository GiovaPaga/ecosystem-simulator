import random


GROWING = 1
NUM_CELLS = 100

CARVIZ_START_ENERGY = 50
CARVIZ_LIFETIME = 100
CARVIZ_AGE = 0

ERBAST_START_ENERGY = 50
ERBAST_LIFETIME = 100
ERBAST_AGE = 0


class Vegetob:
    def __init__(self, density):
        density = range(100)
        self.density = density

    def grow(self, x):
        self.density += x


class Erbast:
    def __init__(self, energy, age, lifetime, social_attitude):
        self.energy = energy
        self.age = age
        self.lifetime = lifetime
        # todo aggiungere range check 0-1
        self.social_attitude = social_attitude


    def movement(self):
        # 1 evaluate if move as group
        # 2 group understand who moves, individual decide if follow the group
        # 3 group apllied decision
        # 4 individuals do opposite of the group
        pass

    def grazing(self):
        pass

    def spawning(self):
        pass


class Carviz:
    def __init__(self, energy, age, lifetime, social_attitude):
        self.energy = energy
        self.age = age
        self.lifetime = lifetime
        # todo aggiungere range check 0-1
        self.social_attitude = social_attitude

    def movement(self):
        pass

    def struggle(self):
        pass

    def spawning(self):
        pass


class Planisus():
    def __init__(self):
        self.num_cells = NUM_CELLS

    #   hint: aggiungere metodo chiamato init_carviz alla classe Planisus che ritorna un set di Carviz e salvarli come membro della class
        self.init_carviz()
        self.init_erbast()
        self.init_vegetob()

    def init_carviz(self):
    # Come generare N carviz e salvarli in una variabile?

        self.all_carviz = []
        N = 100
        for i in range(N):

            CARVIZ_START_SA = round(random.uniform(0.10, 1.00), 2)
            carviz = Carviz(CARVIZ_START_ENERGY, CARVIZ_LIFETIME, CARVIZ_AGE, CARVIZ_START_SA)
            self.all_carviz.append(carviz)
            # all_carviz is the data that you want to save as self.carviz inside Planisus class
    def init_erbast(self):

        self.all_erbast = []
        N = 200
        for i in range(N):
            ERBAST_START_SA = round(random.uniform(0.10, 1.00), 2)
            erbast = Erbast(ERBAST_START_ENERGY, ERBAST_LIFETIME, ERBAST_AGE, ERBAST_START_SA)
            self.all_erbast.append(erbast)

    def init_vegetob(self):
        self.all_vegetob = []
        N = 400
        for i in range(N):
            VEGETOB_START_DENSITY = random.randint(1, 100)
            vegetob = Vegetob(VEGETOB_START_DENSITY)
            self.all_vegetob.append(vegetob)
    def run(self):
        pass

    def run_single_day(self):
        pass

    def set_num_cells(self, num_cells):
        self.num_cells = num_cells


def main():
    planisus = Planisus()
    num_cells = 30
    planisus.set_num_cells(num_cells)
    num_cells = 10
    print(f"Planisus size {planisus.num_cells}x{planisus.num_cells}")


    # 1) Based on what logic do we initialize a set of carviz? Which values of energy, age,
    # lifetime and social attitude do you initialize a single carviz to?
    # Initialization of N carviz based on number of cells;
    # Social attitude random number between 0 and 1
    # energy inialized with number CARVIZ_START_ENERGY
    # lifetime initialize with number CARVIZ_LIFETIME
    # age inialized with number 0

    # 2) Is vegetob and Erbast initalization different from Carviz?
    # Initialization of N erbast based on number of cells (or double of carviz);
    # Social attitude random number between 0 and 1 (ERBAST_START_SA)
    # energy inialized with number ERBAST_START_ENERGY
    # lifetime initialize with number ERBAST_LIFETIME
    # age inialized with number 0

    # Initialization of N vegetob based on number of cells (or double of erbast)
    # density random number between 1 and 100





    # 3) Integrate code above from carviz set generation inside Planisus class




if __name__ == '__main__':
    main()



