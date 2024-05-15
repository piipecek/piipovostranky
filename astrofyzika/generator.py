def generator(prijmeni: str) -> list[int]:
    """
    Generuje seznam 7 čísel v danejch rozmezích.
    """
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
        
        return numbers
    return generate_numbers(prijmeni)