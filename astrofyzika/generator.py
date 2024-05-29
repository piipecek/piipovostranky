import math

def generator(prijmeni: str) -> list[int]:
    """
    Generuje seznam 7 čísel v danejch rozmezích a vypočítá kontrolní číslo
    """
    
    def solver(x1, y1, x2, y2, v1x, v1y, m) -> int:

        # Inicializace parametrů
        v2x, v2y = -v1x, -v1y
        n = 500
        delta_t = 0.05

        # Uložení pozic a rychlostí
        positions_x1 = [x1]
        positions_y1 = [y1]
        positions_x2 = [x2]
        positions_y2 = [y2]

        # Simulace
        for _ in range(n):
            r12x = x2 - x1
            r12y = y2 - y1
            r = math.sqrt(r12x**2 + r12y**2)
            
            a = m / r**2
            a1x = a * r12x / r
            a1y = a * r12y / r
            
            v1x += a1x * delta_t
            v1y += a1y * delta_t
            v2x -= a1x * delta_t
            v2y -= a1y * delta_t
            
            x1 += v1x * delta_t
            y1 += v1y * delta_t
            x2 += v2x * delta_t
            y2 += v2y * delta_t
            
            positions_x1.append(x1)
            positions_y1.append(y1)
            positions_x2.append(x2)
            positions_y2.append(y2)

        # Výpočet kontrolního čísla
        control_number = sum(positions_x1) + sum(positions_x2)
        control_number = round(control_number)
        control_number = int(control_number)
        return control_number
    
    
    def hash_string_to_int(string):
        hash = 0
        for char in string:
            hash = ((hash << 5) - hash) + ord(char)
            hash &= 0xFFFFFFFF  # Convert to 32bit integer
        return hash

    def seeded_random(seed):
        seed = (seed + 0x6d2b79f5) & 0xffffffff
        seed ^= seed >> 15
        seed = (seed * (1 | seed)) & 0xffffffff
        seed ^= seed >> 7
        seed = (seed * (61 | seed)) & 0xffffffff
        seed ^= seed >> 14
        return (seed & 0xffffffff) / 0x100000000

    def generate_numbers(surname):
        seed = hash_string_to_int(surname)
        
        bounds = [
            (-20, 20), # x1
            (60, 100), # y1
            (-20, 20), # x2
            (-100, -60), # y2
            (15, 25), # v1x
            (-5, 5), # v1y
            (8000, 12000), # m
        ]
        
        numbers = []
        for index, (min_val, max_val) in enumerate(bounds):
            rnd = seeded_random(seed + index)
            number = int(rnd * (max_val - min_val + 1)) + min_val
            numbers.append(number)
        numbers.append(solver(*numbers))
        
        
        return numbers
    
    
    return generate_numbers(prijmeni)