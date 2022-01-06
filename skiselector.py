import numpy as np
import argparse

class SkiSelector(object):
    def __init__(self, args):
        # Låste constraints
        #   1. Warburg og Matilde har 2 pers værelset

        # Optional constraints
        #   1. Par er på samme værelse og vælger seng sammen (i.e. tæller som en i lodtrækningen),

        self.pair_couples = args.pair_couples

        self.persons = [
            "Christian",
            "David",
            "Mathias",
            "Charlotte",
            "Kristina",
            "Mark",
            "Thomas",
            "Harald",
            "Gustav",
            "Michala",
            "Matilde",
            "Frederik"
        ]
        self.couples = [
            ("Christian", "Charlotte"),
            ("Thomas", "Kristina"),
            ("Frederik", "Matilde"),
	    ("Mark", "Gustav")
        ]

    def check_constraints(self):
        for couple in self.couples:
            condition = (couple[0] in self.random_perm[:4]) == (couple[1] in self.random_perm[:4])
            if not condition:
                return condition
        return True


    def merge_couple(self, room):
        for couple in self.couples:
            if couple[0] in room and couple[1] in room:
                room = np.delete(room, np.where(room == couple[1]))
        return room

    def assign_rooms(self):
        """
        Assigner et værelses index til hver person
        0 = 2 pers værelse
        1 = 5 pers værelse
        2 = 8 pers værelse
        @return:
        """
        rooms = {
            0: np.array(["Matilde", "Frederik"]),
            1: [],
            2: []
        }

        if not self.pair_couples:
            self.random_perm = np.random.permutation(self.persons[:-2])
        else:
            constraints_fulfilled = False
            while not constraints_fulfilled:
                self.random_perm = np.random.permutation(self.persons[:-2])
                constraints_fulfilled = self.check_constraints()

        rooms[1] = self.random_perm[:4]
        rooms[2] = self.random_perm[4:]

        # Bare for at gøre det kokmpliceret laver vi en ny lodtrækning her på "voting power" i det givne værelse
        # i.e hvilken rækkefølge må man vælge seng i. Hvis det er med pair couples, så stemmer de som 1 person
        # FIXME: Måske er det her dumt da det kan ske der så ikke er en dobbeltseng tilbage når de skal vælge?
        power = {}
        for room_id, room in rooms.items():
            if self.pair_couples:
                power[room_id] = np.random.permutation(self.merge_couple(room))
            else:
                power[room_id] = np.random.permutation(room)

        # Print results
        input("Tryk for at afsløre værelses fordelingen...\n")

        print(f"{'Værelse':<8} {'Personer':<15}")
        for k, v in rooms.items():
            print(f"{k:<8} {'  '.join(v):<15}")

        print("\n")
        input("Tryk for at afsløre hvem som først vælger seng...\n")

        print(f"{'Værelse':<8} {'Power':<15}")
        for k, v in power.items():
            print(f"{k:<8} {'  '.join(v):<15}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ski selector')
    parser.add_argument("--pair_couples", action="store_true", help="Om par skal låses til samme værelse")
    args = parser.parse_args()

    SkiSelector(args).assign_rooms()
