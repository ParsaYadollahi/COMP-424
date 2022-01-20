import random
import math
import statistics


def func1(x, y):
    return math.sin(2*x) + math.cos(y/float(2))


def func2(x, y):
    return math.fabs(x-2) + math.fabs(0.5 * y + 1) - 4


def rand_xy():
    return (random.random() * 10), (random.random() * 10)


def hillClimb(x, y, func, step_size):
    # local hill climg for single point
    max_x, max_y = x, y
    max_value = func(x, y)

    # Trick for all 8 permutations
    for i in range(-1, 2):
        for j in range(-1, 2):

            # value wont do any modification
            if (i == 0 and j == 0):
                continue

            # compute new x and y
            x, y = max_x + i*step_size, j*step_size
            local_max = func1(x, y)

            if x < 0 or x > 10 or y < 0 or y > 10:
                continue
            # compare local max
            if (local_max > max_value):
                max_value = local_max
                max_x, max_y = x, y

    return max_value, max_x, max_y


def local_beam(beams, func, step_size):
    ret_values = []
    for k in range(len(beams)):  # Similar to doing k parallel searchs
        for i in range(-1, 2):
            for j in range(-1, 2):
                x, y = beams[k][0] + i*step_size, beams[k][0] + \
                    j*step_size  # new x and y
                beam_size = func(x, y)
                if x < 0 or y < 0 or x > 10 or y > 10:
                    continue

                ret_values.append([x, y, beam_size])

    return ret_values


def sort_beam(beams):
    beams.sort(key=lambda x: x[2])
    return beams


if __name__ == '__main__':
    step_sizes = [0.01, 0.05, 0.1, 0.2]

    function_xy = func1
    step_size = step_sizes[0]
    global_max = -999

    print('------ HILL ------')
    step_array = []
    for i in range(1, 101):
        x, y = rand_xy()
        local_max = function_xy(x, y)

        count = 1
        # Initial value
        max_value, x, y = hillClimb(x, y, function_xy, step_size)

        # Calculate the global max for the one point
        while(max_value > local_max):
            local_max = max_value
            max_value, x, y = hillClimb(x, y, function_xy, step_size)
            count += 1
        step_array.append(count)

        if (local_max > global_max):
            global_max = local_max

    mean = statistics.mean(step_array)
    std_dev = statistics.stdev(step_array)

    print('Global_max: ', global_max)
    print('Mean: ', mean)
    print('Standard Dev:', std_dev)

    print('------ BEAM ------')
    beam_width = 2
    beams = []
    count = 0
    global_max = -99999999
    step_array = []
    for i in range(100):
        for j in range(beam_width):
            x, y = rand_xy()
            beams.append([x, y, function_xy(x, y)])

        local_max = sort_beam(beams)[-1:][0][2]

        # Produce beams children
        children = local_beam(beams, function_xy, step_size)

        beams = sort_beam(children)[:beam_width]
        value = sort_beam(beams)[-1:][0][2]
        count = 1

        while(value > local_max):
            local_max = value
            children = local_beam(beams, function_xy, step_size)
            beams = sort_beam(children)[:beam_width]
            value = sort_beam(beams)[-1:][0][2]
            count += 1

        step_array.append(count)

        if (local_max > global_max):
            global_max = local_max

    global_max = sort_beam(beams)[-1]
    mean = statistics.mean(step_array)
    std_dev = statistics.stdev(step_array)

    print('Global Max: ', global_max[2])
    print('Mean: ', mean)
    print('Standard Dev:', std_dev)
