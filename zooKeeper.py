# Zookeeper's Challenge

species_codes = {
    "hyena": "Hy",
    "lion": "Li",
    "tiger": "Ti",
    "bear": "Be"
}

id_counters = {
    "hyena": 0,
    "lion": 0,
    "tiger": 0,
    "bear": 0
}

season_dates = {
    "spring": "-03-21",
    "summer": "-06-21",
    "fall": "-09-21",
    "winter": "-12-21"
}

# Load Names

def load_names():
    names = {"hyena": [], "lion": [], "bear": [], "tiger": []}

    with open("animalNames.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    current_species = None

    for line in lines:
        if not line:
            continue

        lower = line.lower()

        # Detect header lines
        if "hyena" in lower and "name" in lower:
            current_species = "hyena"
            continue
        if "lion" in lower and "name" in lower:
            current_species = "lion"
            continue
        if "bear" in lower and "name" in lower:
            current_species = "bear"
            continue
        if "tiger" in lower and "name" in lower:
            current_species = "tiger"
            continue

        # If line contains commas, it's a name list
        if "," in line and current_species:
            names[current_species] = [n.strip() for n in line.split(",")]
            current_species = None

    return names


# Parse Arriving Animal Description

def parse_arriving_line(line):
    line = line.strip()
    parts = [p.strip() for p in line.split(",")]

    # Example first part: "4-year-old female tiger"
    first = parts[0].split()
    age = int(first[0])
    sex = first[-2]
    species = first[-1].lower()

    # birth season
    birth_season = ""
    if "unknown" not in parts[1].lower():
        birth_season = parts[1].replace("born in", "").strip().lower()

    # color
    color = ""
    for p in parts:
        if "color" in p.lower():
            color = p.lower().replace("color", "").strip()
            break

    # weight
    weight = None
    for p in parts:
        if "pound" in p.lower():
            digits = "".join([c for c in p if c.isdigit()])
            weight = int(digits)
            break

    # origin (everything after "from")
    origin = ""
    for p in parts:
        if p.lower().startswith("from"):
            origin = p.replace("from", "").strip()
            break

    return {
        "age": age,
        "sex": sex,
        "species": species,
        "birth_season": birth_season,
        "color": color,
        "weight": weight,
        "origin": origin,
        "arrival_date": "2024-03-26"
    }


# Birth Date Generator

def gen_birth_date(animal):
    year = 2024 - animal["age"]
    s = animal["birth_season"]

    if s in season_dates:
        return f"{year}{season_dates[s]}"
    else:
        return f"{year}-06-01"


# Unique ID Generator

def gen_unique_id(animal):
    sp = animal["species"]
    id_counters[sp] += 1
    return species_codes[sp] + str(id_counters[sp]).zfill(2)


# Assign Name

def assign_name(animal, names):
    sp = animal["species"]
    # Prevent crash if name list empties
    if names[sp]:
        return names[sp].pop(0)
    return f"NoName{str(id_counters[sp]).zfill(2)}"


# Write Report File

def write_report(habitats):
    with open("zooPopulation.txt", "w") as out:
        for species in ["hyena", "lion", "tiger", "bear"]:
            out.write(f"{species.capitalize()} Habitat:\n")
            for a in habitats[species]:
                line = (
                    f"{a['id']}; {a['name']}; birth date: {a['birth_date']}; "
                    f"{a['color']} color; {a['sex']}; {a['weight']} pounds; "
                    f"from {a['origin']}; arrived {a['arrival_date']}\n"
                )
                out.write(line)
            out.write("\n")


# Main

def main():
    names = load_names()

    habitats = {
        "hyena": [],
        "lion": [],
        "tiger": [],
        "bear": []
    }

    with open("arrivingAnimals.txt") as f:
        lines = f.readlines()

    for line in lines:
        animal = parse_arriving_line(line)
        animal["birth_date"] = gen_birth_date(animal)
        animal["id"] = gen_unique_id(animal)
        animal["name"] = assign_name(animal, names)
        habitats[animal["species"]].append(animal)

    write_report(habitats)


if __name__ == "__main__":
    main()
