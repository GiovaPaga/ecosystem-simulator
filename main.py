import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle

#DAYS
DAYS = 1
MONTHS = DAYS*10
YEARS = MONTHS*10
DECADES = YEARS*10
CENTURY = DECADES*10
NUMDAYS = CENTURY * 1
#INITIALIZATION PARAMETERS
NUM_CELLS_H = 100
NUM_CELLS_V = 100
GROUND_PROPORTION = 0.7
ERBAST_PROPORTION = 0.7
CARVIZ_PROPORTION = 0.007
VEGETOB_PROPORTION = 0.5
BORDER_SIZE = 2
NUM_CARVIZ = int(CARVIZ_PROPORTION * GROUND_PROPORTION * NUM_CELLS_V * NUM_CELLS_H)
NUM_ERBAST = int(ERBAST_PROPORTION * GROUND_PROPORTION * NUM_CELLS_V * NUM_CELLS_H)
NUM_VEGETOB = int(VEGETOB_PROPORTION * GROUND_PROPORTION * NUM_CELLS_V * NUM_CELLS_H)
MAX_HERD = 20
MAX_PRIDE = 10
#CREATURE PROPERTIES
GROWING = 1
GRAZING = 1
CREATURE_START_ENERGY = 50
CREATURE_AGE = 0
VEGETOB_START_DENSITY = 20
CREATURE_LIFETIME = 50
MAX_ENERGY = 100
FAILED_HUNT = 1
AGING = 1
#MOVEMENT PROPERTIES
NEIGHBORHOOD = 1
W_VEGETOB = 1
W_CARVIZ = -10

class Vegetob:
    def __init__(self, density):
        assert (density <= 100) and (density >= 0)
        self.density = density

    def grow(self):
        if self.density < 100:
            self.density += GROWING

class Creature:
    def __init__(self, energy, age, lifetime, social_attitude):
        self.energy = energy
        self.age = age
        self.lifetime = lifetime
        self.social_attitude = social_attitude
        self.moving = False
        self.tracked = False


class Erbast(Creature):
    def __init__(self, energy, age, lifetime, social_attitude):
        super().__init__(energy, age, lifetime, social_attitude)

    def grazing(self, vegetob):
        if self.energy < MAX_ENERGY:
            if vegetob.density > 0:
                self.energy += GRAZING
                vegetob.density -= GRAZING

    def spawning(self):
        energy1 = self.energy // 2
        energy2 = self.energy - energy1
        new_erbast1 = Erbast(energy=energy1, age=CREATURE_AGE, lifetime=self.lifetime, social_attitude=self.social_attitude)
        new_erbast2 = Erbast(energy=energy2, age=CREATURE_AGE, lifetime=self.lifetime, social_attitude=self.social_attitude)
        return new_erbast1, new_erbast2

class Carviz(Creature):
    def __init__(self, energy, age, lifetime, social_attitude):
        super().__init__(energy, age, lifetime, social_attitude)

    def spawning(self):
        energy1 = self.energy // 2
        energy2 = self.energy - energy1
        new_carviz1 = Carviz(energy=energy1, age=CREATURE_AGE, lifetime=self.lifetime, social_attitude=self.social_attitude)
        new_carviz2 = Carviz(energy=energy2, age=CREATURE_AGE, lifetime=self.lifetime, social_attitude=self.social_attitude)
        return new_carviz1, new_carviz2


class Planisuss():
    def __init__(self):
        self.matrix = self.init_grid()
        self.carviz_coordinates = self.carviz_grid()
        self.vegetob_coordinates = self.vegetob_grid()
        self.erbast_coordinates = self.erbast_grid()
        #Tracking one random erbast
        random_index = random.randint(0, len(self.erbast_coordinates) - 1)
        random_cell = list(self.erbast_coordinates.keys())[random_index]
        self.erbast_coordinates[random_cell][0].tracked = True

        self.history_days = []
        self.history_erbast = []
        self.history_carviz = []
        self.history_tracked = []

    def record_stats(self, day):
        self.history_days.append(day)
        self.history_erbast.append(sum(len(i) for i in self.erbast_coordinates.values()))
        self.history_carviz.append(sum(len(j) for j in self.carviz_coordinates.values()))
        found = False
        for coords, erbast_list in self.erbast_coordinates.items():
            for erbast in erbast_list:
                if erbast.tracked:
                    self.history_tracked.append(coords)
                    found = True
                    break
            if found:
                break
        if not found:
            self.history_tracked = []
            random_index = random.randint(0, len(self.erbast_coordinates) - 1)
            random_cell = list(self.erbast_coordinates.keys())[random_index]
            self.erbast_coordinates[random_cell][0].tracked = True



    def get_matrix(self):
        return self.matrix

    def carviz_grid(self):
        carviz_coordinates = {}
        while len(carviz_coordinates) < NUM_CARVIZ:
            pos_x = random.randint(0, NUM_CELLS_V - 1)
            pos_y = random.randint(0, NUM_CELLS_H - 1)
            if self.matrix[pos_x, pos_y] == 1:
                carviz_start_sa = round(random.uniform(0, 1), 2)
                carviz = Carviz(CREATURE_START_ENERGY, CREATURE_AGE, CREATURE_LIFETIME, carviz_start_sa)
                carviz_coordinates[(pos_x, pos_y)] = [carviz]
            else:
                continue
        return carviz_coordinates

    def erbast_grid(self):
        erbast_coordinates = {}
        while len(erbast_coordinates) < NUM_ERBAST:
            pos_x = random.randint(0, NUM_CELLS_V - 1)
            pos_y = random.randint(0, NUM_CELLS_H - 1)
            if self.matrix[pos_x, pos_y] == 1:
                erbast_start_sa = round(random.uniform(0, 1), 2)
                erbast = Erbast(CREATURE_START_ENERGY, CREATURE_AGE, CREATURE_LIFETIME, erbast_start_sa)
                erbast_coordinates[(pos_x, pos_y)] = [erbast]
            else:
                continue
        return erbast_coordinates

    def vegetob_grid(self):
        vegetob_coordinates = {}
        for i in range(NUM_CELLS_H):
            for j in range(NUM_CELLS_V):
                if self.matrix[i, j] == 1:
                    vegetob = Vegetob(VEGETOB_START_DENSITY)
                    vegetob_coordinates[(i, j)] = vegetob
        return vegetob_coordinates

    def init_grid(self):
        ground = True
        water = False
        matrix = np.zeros((NUM_CELLS_H, NUM_CELLS_V))
        for i in range(NUM_CELLS_H):
            for j in range(NUM_CELLS_V):
                if i < BORDER_SIZE or i > (NUM_CELLS_V - BORDER_SIZE - 1) or j < BORDER_SIZE or j > (NUM_CELLS_H - BORDER_SIZE - 1):
                    matrix[i, j] = water
                else:
                    x = np.random.uniform(0.0, 1.0)
                    if x > (1 - GROUND_PROPORTION):
                        matrix[i, j] = ground
                    else:
                        matrix[i, j] = water
        return matrix

    def growing(self):
        for coordinates, vegetob in self.vegetob_coordinates.items():
            vegetob.grow()
        # Check overwhelming
        for coordinates in list(self.vegetob_coordinates.keys()):
            pos_x, pos_y = coordinates
            neighbor_cells = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),  (1, 0), (1, 1)]   # surrounding cells
            surrounded = True
            for x, y in neighbor_cells:
                nx, ny = pos_x + x, pos_y + y
                # check if all surrounding cells are with max density or water
                if (nx, ny) in self.vegetob_coordinates and self.vegetob_coordinates[(nx, ny)].density < 100:
                    surrounded = False
                    break
            # killing overwhelmed creatures
            if surrounded:
                self.carviz_coordinates.pop(coordinates, None)
                self.erbast_coordinates.pop(coordinates, None)
        return self.vegetob_coordinates

    def erbast_movement(self):
        new_erbast = {}
        for current_coords, erbast_herd in self.erbast_coordinates.items():
            pos_x, pos_y = current_coords
            neighbor_cells = [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            best_score = -9999
            best_coords = current_coords
            valid_neighbors = []
            for x, y in neighbor_cells:
                nx, ny = pos_x + x, pos_y + y
                if (nx, ny) in self.vegetob_coordinates:
                    valid_neighbors.append((nx, ny))
                    cell_density = self.vegetob_coordinates[(nx, ny)].density
                    num_carviz = 0
                    if (nx, ny) in self.carviz_coordinates:
                        num_carviz = len(self.carviz_coordinates[(nx, ny)])
                    # Defining score for every cell
                    score = (cell_density * W_VEGETOB) + (num_carviz * W_CARVIZ)
                    if score > best_score:
                        best_score = score
                        best_coords = (nx, ny)
            for i, erbast in enumerate(erbast_herd):
                random_num = random.random()
                if i >= MAX_HERD:
                    random_num = 1
                if random_num <= erbast.social_attitude:
                    destination = best_coords
                else:
                    if best_coords != current_coords:
                        destination = current_coords
                    else:
                        run_cells = []
                        for cell in valid_neighbors:
                            if cell != current_coords:
                                run_cells.append(cell)
                        if len(run_cells) > 0:
                            destination = random.choice(run_cells)
                        else:
                            destination = current_coords
                if destination != current_coords:
                    erbast.energy -= 1
                    erbast.moving = True
                else:
                    erbast.moving = False
                if erbast.energy > 0:
                    if destination not in new_erbast:
                        new_erbast[destination] = [erbast]
                    else:
                        new_erbast[destination].append(erbast)
        self.erbast_coordinates = new_erbast
        return self.erbast_coordinates

    def carviz_movement(self):
        new_carviz = {}
        for current_coords, carviz_pride in self.carviz_coordinates.items():
            pos_x, pos_y = current_coords
            neighbor_cells = [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            best_score = -9999
            best_coords = current_coords
            valid_neighbors = []
            for x, y in neighbor_cells:
                nx, ny = pos_x + x, pos_y + y
                if (nx, ny) in self.vegetob_coordinates:
                    valid_neighbors.append((nx, ny))
                    num_erbast = 0
                    if (nx, ny) in self.erbast_coordinates:
                        num_erbast = len(self.erbast_coordinates[(nx, ny)])
                    score = num_erbast
                    if score > best_score:
                        best_score = score
                        best_coords = (nx, ny)
            for i, carviz in enumerate(carviz_pride):
                random_num = random.random()
                if i >= MAX_PRIDE:
                    random_num = 1
                if random_num <= carviz.social_attitude:
                    destination = best_coords
                else:
                    if best_coords != current_coords:
                        destination = current_coords
                    else:
                        run_cells = []
                        for cell in valid_neighbors:
                            if cell != current_coords:
                                run_cells.append(cell)
                        if len(run_cells) > 0:
                            destination = random.choice(run_cells)
                        else:
                            destination = current_coords
                if destination != current_coords:
                    carviz.energy -= 1
                    carviz.moving = True
                else:
                    carviz.moving = False
                if carviz.energy > 0:
                    if destination not in new_carviz:
                        new_carviz[destination] = {}
                    if current_coords not in new_carviz[destination]:
                        new_carviz[destination][current_coords] = []
                    new_carviz[destination][current_coords].append(carviz)
        post_movement_carviz = {}
        for dest, origin_groups in new_carviz.items():
            post_movement_carviz[dest] = list(origin_groups.values())
        return post_movement_carviz

    def grazing(self):
        for coords, erbast_list in self.erbast_coordinates.items():
            if coords in self.vegetob_coordinates:
                vegetob = self.vegetob_coordinates[coords]
                len_group = len(erbast_list)
                # bubble sort for erbast energy
                for i in range(len_group):
                    for j in range(len_group - i - 1):
                        if erbast_list[j].energy > erbast_list[j + 1].energy:
                            erbast_list[j], erbast_list[j + 1] = erbast_list[j + 1], erbast_list[j]
                for erbast in erbast_list:
                    if not erbast.moving and vegetob.density > 0 and erbast.energy < 100:
                        erbast.grazing(vegetob)
                    elif vegetob.density == 0:
                        break
        return self.erbast_coordinates

    def carviz_struggle(self, post_movement_carviz):
        resolved_carviz_coordinates = {}
        for coords, arriving_prides in post_movement_carviz.items():
            winning_pride = []
            if len(arriving_prides) > 1:
                winning_pride = self.fight(arriving_prides)
            elif arriving_prides:
                winning_pride = arriving_prides[0]
            if winning_pride:
                self.hunt(coords, winning_pride)
                resolved_carviz_coordinates[coords] = winning_pride
        self.carviz_coordinates = resolved_carviz_coordinates
        for coords in list(self.erbast_coordinates.keys()):
            if len(self.erbast_coordinates[coords]) == 0:
                del self.erbast_coordinates[coords]


    def fight(self, arriving_prides):
        merged_pride = arriving_prides.pop(0)
        for incoming_pride in arriving_prides:
            avg_sa_merged = sum(carviz.social_attitude for carviz in merged_pride) / len(merged_pride)
            avg_sa_incoming = sum(carviz.social_attitude for carviz in incoming_pride) / len(incoming_pride)
            join_chance = (avg_sa_merged + avg_sa_incoming) / 2
            if random.random() < join_chance:
                merged_pride.extend(incoming_pride)
            else:
                energy_merged = sum(carviz.energy for carviz in merged_pride)
                energy_incoming = sum(carviz.energy for carviz in incoming_pride)
                total_energy = energy_merged + energy_incoming
                if total_energy == 0:
                    if random.random() < 0.5:
                        merged_pride = incoming_pride
                else:
                    win_probability_incoming = energy_incoming / total_energy

                    if random.random() < win_probability_incoming:
                        merged_pride = incoming_pride
        return merged_pride

    def hunt(self, coords, pride):
        herd = self.erbast_coordinates.get(coords)
        if not herd or len(herd) == 0:
            return
        max_energy = max(erbast.energy for erbast in herd)
        strongest_erbast = None
        for erbast in herd:
            if erbast.energy == max_energy:
                strongest_erbast = erbast
                break
        pride_energy = sum(carviz.energy for carviz in pride)
        prey_energy = strongest_erbast.energy
        total_power = pride_energy + prey_energy
        pride_win = False
        if total_power > 0:
            success_chance = pride_energy / total_power
            if random.random() < success_chance:
                pride_win = True
        if pride_win:
            herd.remove(strongest_erbast)
            if pride and len(pride) > 0:
                n = len(pride)  # bubble sort
                for i in range(n):
                    for j in range(0, n - i - 1):
                        if pride[j].energy > pride[j + 1].energy:
                            pride[j], pride[j + 1] = pride[j + 1], pride[j]
                energy_divided = prey_energy // len(pride)
                remaining_energy = prey_energy % len(pride)
                for carviz in pride:
                    carviz.energy += energy_divided
                for i in range(remaining_energy):
                    pride[i].energy += 1
        else:
            if pride:
                for carviz in pride:
                    carviz.energy -= FAILED_HUNT
                    if carviz.energy > MAX_ENERGY:
                        carviz.energy = MAX_ENERGY

    def erbast_spawning(self):
        for erbast_list in list(self.erbast_coordinates.values()):
            for erbast in list(erbast_list):
                erbast.age += 1
                if erbast.age % 10 == 0:
                    erbast.energy -= AGING
                if erbast.energy <= 0:
                    erbast_list.remove(erbast)
                    continue
                if erbast.age >= erbast.lifetime:
                    if len(erbast_list) + 1 <= MAX_HERD:
                        new_erbast1, new_erbast2 = erbast.spawning()
                        erbast_list.append(new_erbast1)
                        erbast_list.append(new_erbast2)
                    erbast_list.remove(erbast)
        for coords in list(self.erbast_coordinates.keys()):
            if len(self.erbast_coordinates[coords]) == 0:
                del self.erbast_coordinates[coords]

        return self.erbast_coordinates

    def carviz_spawning(self):
        for carviz_list in list(self.carviz_coordinates.values()):
            for carviz in list(carviz_list):
                carviz.age += 1
                if carviz.age % 10 == 0:
                    carviz.energy -= AGING
                if carviz.energy <= 0:
                    carviz_list.remove(carviz)
                    continue
                if carviz.age >= carviz.lifetime:
                    if len(carviz_list) + 1 <= MAX_PRIDE:
                        new_carviz1, new_carviz2 = carviz.spawning()
                        carviz_list.append(new_carviz1)
                        carviz_list.append(new_carviz2)
                    carviz_list.remove(carviz)
        for coords in list(self.carviz_coordinates.keys()):
            if len(self.carviz_coordinates[coords]) == 0:
                del self.carviz_coordinates[coords]

        return self.carviz_coordinates

    def run_single_day(self):
        self.growing()
        self.erbast_movement()
        post_movement_carviz = self.carviz_movement()
        self.carviz_struggle(post_movement_carviz)
        self.grazing()
        self.erbast_spawning()
        self.carviz_spawning()
        self.record_stats(len(self.history_days))

    def get_rgb_map(self):
        rgb = np.zeros((NUM_CELLS_H, NUM_CELLS_V, 3))
        max_carviz = max((len(v) for v in self.carviz_coordinates.values()), default=1)
        max_erbast = max((len(v) for v in self.erbast_coordinates.values()), default=1)
        for i in range(NUM_CELLS_H):
            for j in range(NUM_CELLS_V):
                if self.matrix[i, j] == 0:
                    rgb[i, j] = (0, 0, 0.3)
                else:
                    rgb[i, j, 0] = len(self.carviz_coordinates.get((i, j), [])) / max_carviz
                    rgb[i, j, 1] = len(self.erbast_coordinates.get((i, j), [])) / max_erbast
                    rgb[i, j, 2] = 0.5 + (self.vegetob_coordinates.get((i, j), Vegetob(0)).density/100) * 0.5
        return rgb


def main():
    world = [Planisuss()]
    fig, (ax_map, ax_plot) = plt.subplots(1, 2, figsize=(12, 5))
    line_erbast, = ax_plot.plot([], [], color='green', label='Erbast')
    line_carviz, = ax_plot.plot([], [], color='red', label='Carviz')
    ax_plot.legend()
    img = ax_map.imshow(world[0].get_rgb_map(), vmin=0, vmax=1, interpolation='nearest')
    line_tracked, = ax_map.plot([], [], color='yellow', linewidth=1)
    paused = [False]

    def update(frame):
        if not paused[0] and len(world[0].history_days) < NUMDAYS:
            world[0].run_single_day()
            img.set_data(world[0].get_rgb_map())
            line_erbast.set_data(world[0].history_days, world[0].history_erbast)
            line_carviz.set_data(world[0].history_days, world[0].history_carviz)
            ax_plot.relim()
            ax_plot.autoscale_view()
            x = [coord[0] for coord in world[0].history_tracked]
            y = [coord[1] for coord in world[0].history_tracked]
            line_tracked.set_data(y, x)
        return [img, line_erbast, line_carviz, line_tracked]
    def click(event):
        if event.inaxes == ax_map:
            col = int(event.xdata)
            row = int(event.ydata)
            num_erbast = len(world[0].erbast_coordinates.get((row, col), []))
            num_carviz = len(world[0].carviz_coordinates.get((row, col), []))
            veg = world[0].vegetob_coordinates.get((row, col))
            density = veg.density if veg else 0
            ax_map.set_title(f"Cell ({row},{col}) — Erbast: {num_erbast}, Carviz: {num_carviz}, Vegetob: {density}")
            fig.canvas.draw()
    def on_key(event):
        if event.key == ' ':
            paused[0] = not paused[0]
        elif event.key == 's':
            f = open('savefile.pkl', 'wb')
            pickle.dump(world[0], f)
            f.close()
        elif event.key == 'l':
            f = open('savefile.pkl', 'rb')
            world[0] = pickle.load(f)
            f.close()
            img.set_data(world[0].get_rgb_map())
            ax_map.set_xlim(0, NUM_CELLS_V)
            ax_map.set_ylim(NUM_CELLS_H, 0)
            line_erbast.set_data(world[0].history_days, world[0].history_erbast)
            line_carviz.set_data(world[0].history_days, world[0].history_carviz)
            ax_plot.relim()
            ax_plot.autoscale_view()
            fig.canvas.draw()
    fig.canvas.mpl_connect('key_press_event', on_key)
    fig.canvas.mpl_connect('button_press_event', click)
    ani= animation.FuncAnimation(fig, update, interval=100, cache_frame_data=False, blit=True)
    plt.show()

if __name__ == "__main__":
    main()





