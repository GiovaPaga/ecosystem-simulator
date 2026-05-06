# Planisuss

**Agent-based predator-prey simulation in Python**, developed as the final 
project for the *Computer Programming, Algorithms and Data Structures (Mod. 1)* 
course at the University of Pavia (BSc in Artificial Intelligence, A.Y. 2022/23).

The simulation models a fictitious world inhabited by three interacting species
on a 2D grid, with object-oriented agents, social-group dynamics, and real-time 
interactive visualization. The project is freely inspired by Conway's *Game of 
Life* and the *Wa-Tor* predator-prey simulation, extended with multiple 
trophic levels, heterogeneous agents, and group decision-making.

> *Project specification by Prof. Stefano Ferrari (University of Pavia). 
> Implementation, design choices, and visualization by Giovanni Pagani.*

---

## Overview

Planisuss is a square grid populated by three species:

- **Vegetob** — vegetation, grows spontaneously, food source for Erbast.
- **Erbast** — herbivores, eat Vegetob, group into *herds*, can move and reproduce.
- **Carviz** — carnivores, hunt Erbast, group into *prides*, fight over territory.

Each simulated *day* consists of five phases: **Growing**, **Movement**, 
**Grazing**, **Struggle** (fight or hunt), and **Spawning**. The interaction 
of these phases produces emergent population dynamics qualitatively similar 
to classic Lotka-Volterra oscillations.

---

## Features

- **Object-oriented agent design** — `Creature` base class with `Erbast` and 
  `Carviz` subclasses; separate `Vegetob` and `Planisus` (world) classes.
- **Heterogeneous agents** — every individual has its own *energy*, *age*, 
  *lifetime*, and *social attitude* (a value in [0, 1] that modulates 
  individual vs. group behavior).
- **Utility-based movement** — herds and prides evaluate neighboring cells 
  via a weighted score combining vegetation density and predator presence.
- **Probabilistic combat** — when multiple prides reach the same cell, they 
  may merge or fight; outcomes are stochastic and weighted by cumulative 
  energy.
- **Hunting mechanics** — prides target the strongest prey in the cell; 
  hunt success depends on the energy ratio between pride and prey.
- **Life cycle** — agents age, lose energy over time, and reproduce by 
  splitting at end of life (offspring inherit averaged properties).
- **Carrying capacity** — `MAX_HERD` and `MAX_PRIDE` limit group size, 
  preventing population divergence.
- **Real-time visualization** — animated map (Matplotlib) plus live 
  population plot; one randomly selected Erbast is tracked across the map.
- **Interactive controls** — pause/resume, save/load simulation state 
  (pickle), click on any cell to inspect its contents.

---

## Demo

[Optional: insert a GIF of the simulation here once recorded.]
[Optional: insert a screenshot of the population dynamics plot.]

---

## How to Run

Requires Python 3.10+.

Clone the repository and install dependencies:

    git clone git@github.com:giovapaga/ecosystem-simulator.git
    cd ecosystem-simulator
    pip install -r requirements.txt

Run the simulation:

    python main.py

---

## Controls

| Key / Action | Effect |
|---|---|
| **Spacebar** | Pause / resume simulation |
| **S** | Save current state to `savefile.pkl` |
| **L** | Load state from `savefile.pkl` |
| **Click on cell** | Show cell contents (number of Erbast, Carviz, Vegetob density) |

---

## Implementation Notes

A few design decisions worth highlighting:

- **Movement scoring.** Erbast evaluate cells with a linear utility function 
  `score = W_VEGETOB * density + W_CARVIZ * num_carviz`, choosing the cell 
  with the highest score. Carviz instead score on prey availability.
- **Social attitude.** Each individual draws a random number against its own 
  social attitude to decide whether to follow the group or act alone — 
  introducing within-group heterogeneity even when herds/prides share the 
  same nominal strategy.
- **Pride struggle.** When multiple prides arrive at the same cell, they 
  merge probabilistically (weighted by average social attitude) or fight 
  (winning probability proportional to total energy). This tends to 
  produce stable dominant prides over time.

---

## Possible Extensions

Ideas I'd like to explore in future revisions:

- Replace the fixed `social_attitude` parameter with a small reinforcement 
  learning agent that learns when to follow the group vs. act independently.
- Sensitivity analysis: systematically vary `W_CARVIZ`, `GROWING`, and 
  `MAX_HERD` to map regimes of stable coexistence vs. extinction.
- Modular refactor: split the single-file implementation into 
  `creatures.py`, `world.py`, `visualization.py`, `config.py`.
- Unit tests with pytest covering core mechanics (energy decay, spawning 
  rules, hunt outcomes).

---

## Acknowledgments

Project specification: Prof. Stefano Ferrari, University of Pavia, 
*Computer Programming, Algorithms and Data Structures (Mod. 1)*, 
A.Y. 2022/23.

Inspired by:
- A. K. Dewdney, *"Computer recreations: Sharks and fish wage an 
  ecological war on the toroidal planet Wa-Tor"*, Scientific American, 1984.
- M. Gardner, *"The fantastic combinations of John Conway's new solitaire 
  game 'Life'"*, Scientific American, 1970.

---

## Author

**Giovanni Pagani** — BSc student in Artificial Intelligence, 
University of Pavia / Milano-Bicocca / Statale.

[LinkedIn](https://www.linkedin.com/in/giovannipagani) · 
[GitHub](https://github.com/giovapaga)
