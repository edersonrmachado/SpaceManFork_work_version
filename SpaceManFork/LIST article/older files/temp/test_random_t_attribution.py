import random


def generate_values(t_start, t_end, number_of_points, min_distance):
    if t_end - t_start < (number_of_points - 1) * min_distance:
        raise ValueError("There is not enough space to generate the values.")

    values = []

    # Remaining space after reserving the minimum distances
    remaining_space = ((t_end - t_start)- (number_of_points - 1) * min_distance)

    # Generate random points
    random_points = sorted(round(random.uniform(0, remaining_space),3)
        for _ in range(number_of_points))

    for i, point in enumerate(random_points):
        values.append(t_start + point + i * min_distance)

    return values


number_of_points = 100
t_start = 0
t_end = t_start + 172800
min_distance = 4

values = generate_values(
    t_start,
    t_end,
    number_of_points,
    min_distance
)

print(values)

