
import itertools
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# all possible (not so bad) solutions
possible_solutions = [ ]

# # Function to calculate the distance between two points
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

cm = (10., 5.)
threshold = 0.5

def calc_crx(data, pillars):
    ix = data[pillars][:,14]
    ix_xr = data[pillars][:,17]
    sum_ix = sum(ix)
    sum_ix_xr = sum(ix_xr)
    return sum_ix_xr / sum_ix


def calc_cry(data, pillars):
    iy = data[pillars][:,15]
    iy_yr = data[pillars][:,16]
    sum_iy = sum(iy)
    sum_iy_yr = sum(iy_yr)
    return sum_iy_yr / sum_iy

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

# # Pruning function example: check if the current combination has at least two points 
# # and if the distance between them is within a certain range
def pruning_rule(values, combination):
    combination = [int(x) for x in combination]
    crx = calc_crx(values, combination)
    cry = calc_cry(values, combination)
    return abs(crx - cm[0]) <= 3 and abs(cry-cm[1]) <= 1.5
    return euclidean_distance( (crx, cry), cm ) < threshold
    if len(combination) < 2:
        return False
    for p1, p2 in itertools.combinations(combination, 2):
        if distance(p1, p2) < 1 or distance(p1, p2) > 10:  # Adjust the range as needed
            return False
    return True

# # Recursive backtracking function to find the optimal combination
def find_smart_solutions(points, k, current_combination, index, just_added=False):
    # global possible_solutions
    if len(current_combination) > k[1]:
        return None, float('-inf')

    if len(current_combination) + (len(points)-index) < k[0]:
        return None, float('-inf')
    
    if len(current_combination) >= k[0]: 
        if pruning_rule(points, current_combination) == False:
            return None, float('-inf')
        
    if just_added:
        # if pruning_rule(points, current_combination):
            if k[0] <= len(current_combination) <= k[1]:    
                possible_solutions.append(current_combination.copy())


    if index == len(points):
        return None, float('-inf')
    # if len(current_combination) >= k[0]:
    #     if pruning_rule(points, current_combination) == False:
    #         return None, float('-inf')
    #     else:

    # Try including the current point
    current_combination.append(index)
    find_smart_solutions(points, k, current_combination, index + 1, True)
    current_combination.pop()
    find_smart_solutions(points, k, current_combination, index + 1, False)


def read_points_from_csv(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    df = df.sample(frac=1)
    values = np.array(df.values)
    # print(values[1])
    return values

def plot_points(points):
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plt.scatter(x, y)
    plt.show()


values = read_points_from_csv("./plan.csv")

for i in range(len(values)):
    values[i][0] = int(values[i][0])

half_values = values[:20:]

n = len(half_values)
m = len(half_values[0])

print(f"{n} rows")
print(f"{m} columns")

k = (int(.6*n), int(.7*n))
# k = (1, 23)

smart_solutions = find_smart_solutions(half_values, k, [], 0)

num_possible_solutions = len(possible_solutions)
all_solutions = 2 ** n
print(f"valid solutions: {num_possible_solutions}")
print(f"all solutions: {all_solutions}")
print(f"valid solutions %: {round(num_possible_solutions/all_solutions*100,2)}")
print("-"*20)

SOLUTION_INDEX = 0
solution = half_values[possible_solutions[SOLUTION_INDEX]]

print("Solution:")
print(sorted([int(x) for x in solution[:,0]]))

points_to_plot = solution[:,10:12]
# print(half_values[solution][:,10:12])

plot_points(points_to_plot)