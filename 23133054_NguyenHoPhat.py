import pygame
import time
import sys
import heapq
from collections import deque
import math
import random
from enum import Enum
#region [Cấu hình và hằng số]
WIDTH, HEIGHT = 800, 750
GRID_SIZE = 3
TILE_SIZE = (WIDTH - 300) // GRID_SIZE
FONT_SIZE = 40
STEP_DELAY = 300
BUTTON_COLS = 6
BUTTON_SIZE = WIDTH // BUTTON_COLS - 10

COLORS = {
    "background": (30, 30, 30),
    "tile": (100, 100, 250),
    "text": (255, 255, 255),
    "button": {
        "BFS": (241, 76, 76),
        "A*": (76, 241, 76),
        "Greedy": (76, 76, 241),
        "IDDFS": (241, 241, 76),
        "IDA*": (241, 76, 241),
        "Hill": (76, 241, 241),
        "Steepest": (178, 102, 255),
        "default": (70, 70, 70),
        "UCS": (12,12,12),
        "Beam": (255, 165, 0),
        "SA": (128, 0, 128),
        "Genetic": (0, 255, 127),
        "IDDFS": (255, 192, 203)
    }
}

goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#endregion

#region [Các lớp cơ bản]
class PuzzleSolver:
    def solve(self, start, goal):
        raise NotImplementedError

class HeuristicSolver(PuzzleSolver):
    def heuristic(self, state):
        distance = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = state[i][j]
                if value != 0:
                    goal_row = (value - 1) // GRID_SIZE
                    goal_col = (value - 1) % GRID_SIZE
                    distance += abs(i - goal_row) + abs(j - goal_col)
        return distance


#endregion

#region [Các thuật toán cụ thể]

class GeneticSolver(PuzzleSolver):
    def __init__(self, population_size=200, generations=500, mutation_rate=0.2, chromosome_length=30):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.chrom_len = chromosome_length
        self.moves = directions  # [(0,1),(0,-1),(1,0),(-1,0)]

    def solve(self, start, goal):
        # Hamming distance làm fitness
        def fitness(state):
            mismatches = sum(
                1 for i in range(GRID_SIZE) for j in range(GRID_SIZE)
                if state[i][j] != 0 and state[i][j] != goal[i][j]
            )
            return mismatches

        def apply_moves(state, moves):
            s = state
            for dx, dy in moves:
                br, bc = find_blank(s)
                nr, nc = br + dx, bc + dy
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    s = swap_tiles(s, br, bc, nr, nc)
            return s

        def random_chromosome():
            return [random.choice(self.moves) for _ in range(self.chrom_len)]

        def crossover(a, b):
            cut = random.randint(1, self.chrom_len - 2)
            return a[:cut] + b[cut:]

        def mutate(chrom):
            return [random.choice(self.moves) if random.random() < self.mutation_rate else m 
                    for m in chrom]

        # Khởi tạo quần thể
        population = [random_chromosome() for _ in range(self.population_size)]

        for gen in range(self.generations):
            # Đánh giá và sort theo fitness
            scored = []
            for chrom in population:
                state = apply_moves(start, chrom)
                score = fitness(state)
                if score == 0:
                    # rebuild path và trả về
                    path = [start]
                    for m in chrom:
                        br, bc = find_blank(path[-1])
                        nr, nc = br + m[0], bc + m[1]
                        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                            path.append(swap_tiles(path[-1], br, bc, nr, nc))
                            if path[-1] == goal:
                                return path
                    return path
                scored.append((score, chrom))
            scored.sort(key=lambda x: x[0])
            # Elitism: giữ 20% best
            top_k = [chrom for _, chrom in scored[:self.population_size // 5]]

            # Sinh thế hệ mới
            new_pop = []
            while len(new_pop) < self.population_size:
                p1, p2 = random.sample(top_k, 2)
                child = crossover(p1, p2)
                child = mutate(child)
                new_pop.append(child)
            population = new_pop

        # Nếu hết thế hệ mà chưa tìm ra
        return None

class BFSSolver(PuzzleSolver):
    def solve(self, start, goal):
        queue = deque([(start, [])])
        visited = set()
        while queue:
            state, path = queue.popleft()
            if state == goal:
                return path + [state]
            blank = find_blank(state)
            for dx, dy in directions:
                nx, ny = blank[0] + dx, blank[1] + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    new_state = swap_tiles(state, *blank, nx, ny)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, path + [new_state]))
        return None

class AStarSolver(HeuristicSolver):
    def solve(self, start, goal):
        heap = [(0 + self.heuristic(start), 0, start, [])]
        visited = set()
        while heap:
            f, g, state, path = heapq.heappop(heap)
            if state == goal:
                return path + [state]
            if state in visited:
                continue
            visited.add(state)
            blank = find_blank(state)
            for dx, dy in directions:
                nx, ny = blank[0] + dx, blank[1] + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    new_state = swap_tiles(state, *blank, nx, ny)
                    new_g = g + 1
                    new_f = new_g + self.heuristic(new_state)
                    heapq.heappush(heap, (new_f, new_g, new_state, path + [new_state]))
        return None



class IDDFSSolver(PuzzleSolver):
    def solve(self, start, goal, max_depth=30):
 
        for depth in range(max_depth + 1):  # Bao gồm cả max_depth
            result = self._depth_limited_dfs(start, goal, depth)
            if result is not None:
                return result
        return None

    def _depth_limited_dfs(self, start, goal, depth_limit):
        stack = [(start, [start])]  # Lưu cả path để theo dõi
        visited = set()
        visited.add(self._state_to_tuple(start))
        
        while stack:
            state, path = stack.pop()
            
            # Kiểm tra goal state trước khi xử lý
            if state == goal:
                return path
            
            # Bỏ qua nếu đã đạt đến giới hạn độ sâu
            if len(path) - 1 >= depth_limit:  # path[0] là start state
                continue
                
            blank = find_blank(state)
            
            # Tạo các trạng thái kế tiếp theo thứ tự ngược để duyệt đúng DFS
            for dx, dy in reversed(directions):  # Đảo ngược để duyệt đúng thứ tự
                nx, ny = blank[0] + dx, blank[1] + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    new_state = swap_tiles(state, *blank, nx, ny)
                    state_tuple = self._state_to_tuple(new_state)
                    
                    if state_tuple not in visited:
                        visited.add(state_tuple)
                        stack.append((new_state, path + [new_state]))
        
        return None

    def _state_to_tuple(self, state):
        return tuple(tuple(row) for row in state)
class GreedySolver(HeuristicSolver):
    def solve(self, start, goal):
        heap = [(self.heuristic(start), start, [])]
        visited = set()
        while heap:
            h, state, path = heapq.heappop(heap)
            if state == goal:
                return path + [state]
            if state in visited:
                continue
            visited.add(state)
            blank = find_blank(state)
            for dx, dy in directions:
                nx, ny = blank[0] + dx, blank[1] + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    new_state = swap_tiles(state, *blank, nx, ny)
                    heapq.heappush(heap, (self.heuristic(new_state), new_state, path + [new_state]))
        return None

from copy import deepcopy
import random

class HillClimbingSolver(HeuristicSolver):
    def solve(self, start, goal, max_attempts=1000, allow_sideways=False, max_sideways=5, max_visited=10000):
        current = deepcopy(start)
        path = [deepcopy(current)]
        visited = set()
        visited.add(self._state_to_tuple(current))
        attempts = 0
        sideways_moves = 0
        
        while attempts < max_attempts:
            if self._state_to_tuple(current) == self._state_to_tuple(goal):
                return path

            neighbors = self._get_unvisited_neighbors(current, visited)
            if not neighbors:
                break  # No more moves

            best_neighbor = min(neighbors, key=lambda x: self.heuristic(x))
            current_h = self.heuristic(current)
            best_h = self.heuristic(best_neighbor)

            # Allow sideways moves (equal heuristic) to escape plateaus
            if best_h > current_h or (best_h == current_h and not allow_sideways):
                break  # No better or allowed sideways move
            elif best_h == current_h:
                sideways_moves += 1
                if sideways_moves > max_sideways:
                    break  # Too many sideways moves, restart or terminate
            else:
                sideways_moves = 0  # Reset on improvement

            # Check if best_neighbor is the goal before moving
            if self._state_to_tuple(best_neighbor) == self._state_to_tuple(goal):
                path.append(deepcopy(best_neighbor))
                return path

            current = best_neighbor
            path.append(deepcopy(current))
            visited.add(self._state_to_tuple(current))
            
            # Limit visited set size to prevent memory issues
            if len(visited) > max_visited:
                visited.pop()  # Remove oldest entry (if order matters)

            attempts += 1

        return path if self._state_to_tuple(current) == self._state_to_tuple(goal) else None

    def _get_unvisited_neighbors(self, state, visited):
        neighbors = []
        blank = find_blank(state)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dx, dy in directions:
            nx, ny = blank[0] + dx, blank[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                new_state = swap_tiles(deepcopy(state), blank[0], blank[1], nx, ny)
                state_tuple = self._state_to_tuple(new_state)
                if state_tuple not in visited:
                    neighbors.append(new_state)
        return neighbors

    def _state_to_tuple(self, state):
        return tuple(tuple(row) for row in state)
class SimulatedAnnealingSolver(HeuristicSolver):
    def solve(self, start, goal):
        current = start
        current_cost = self.heuristic(current)
        temperature = 100.0
        cooling_rate = 0.99
        min_temperature = 0.1
        max_steps = 10000

        path = [current]

        for step in range(max_steps):
            if current == goal:
                return path

            neighbors = self.get_neighbors(current)
            if not neighbors:
                break

            next_state = random.choice(neighbors)
            next_cost = self.heuristic(next_state)

            delta = next_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current = next_state
                current_cost = next_cost
                path.append(current)

            temperature *= cooling_rate
            if temperature < min_temperature:
                break

        return path if current == goal else None

    def get_neighbors(self, state):
        blank = find_blank(state)
        neighbors = []
        for dx, dy in directions:
            nx, ny = blank[0] + dx, blank[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                new_state = swap_tiles(state, *blank, nx, ny)
                neighbors.append(new_state)
        return neighbors

class BeamSearchSolver(HeuristicSolver):
    def __init__(self, beam_width=2):  # Thêm hàm khởi tạo
        self.beam_width = beam_width
        
    def solve(self, start, goal):  # Bỏ tham số beam_width ở đây
        current_level = [(self.heuristic(start), start, [start])]
        visited = set()
        while current_level:
            next_level = []
            for h, state, path in current_level:
                if state == goal:
                    return path
                blank = find_blank(state)
                neighbors = []
                for dx, dy in directions:
                    nx, ny = blank[0] + dx, blank[1] + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        new_state = swap_tiles(state, *blank, nx, ny)
                        if new_state not in visited:
                            new_h = self.heuristic(new_state)
                            new_path = path + [new_state]
                            neighbors.append((new_h, new_state, new_path))
                            visited.add(new_state)
                neighbors.sort()
                next_level.extend(neighbors[:self.beam_width])  # Sử dụng self.beam_width
            current_level = sorted(next_level, key=lambda x: x[0])[:self.beam_width]
        return None
#endregion
class DFSSolver(PuzzleSolver):
    def solve(self, start, goal, depth_limit=100):
        stack = [(start, [])]
        visited = set()
        while stack:
            state, path = stack.pop()
            if state == goal:
                return path + [state]
            if len(path) > depth_limit:
                continue
            if state in visited:
                continue
            else:
                visited.add(state)
            blank = find_blank(state)
            for dx, dy in directions:
                nx, ny = blank[0] + dx, blank[1] + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    new_state = swap_tiles(state, *blank, nx, ny)
                    stack.append((new_state, path + [new_state]))
        return None

class UCSolver(PuzzleSolver):
    def solve(self, start, goal):
        heap = [(0, start, [])]
        visited = set()
        while heap:
            cost, state, path = heapq.heappop(heap)
            if state == goal:
                return path + [state]
            if state in visited:
                continue
            visited.add(state)
            blank = find_blank(state)
            for dx, dy in directions:
                nx, ny = blank[0] + dx, blank[1] + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    new_state = swap_tiles(state, *blank, nx, ny)
                    heapq.heappush(heap, (cost + 1, new_state, path + [new_state]))
        return None

import random
from math import exp

class StochasticHillClimbingSolver(HeuristicSolver):
    def solve(self, start, goal, max_steps=1000, temperature=1.0, cooling_rate=0.99):
        current = start
        best_state = current
        best_h = self.heuristic(current)
        path = [current]
        visited = set()
        visited.add(self._state_to_tuple(current))
        
        for step in range(max_steps):
            if current == goal:
                return path
            
            # Tạo danh sách các trạng thái kề chưa xét
            neighbors = self._get_unvisited_neighbors(current, visited)
            
            if not neighbors:
                # Thử random restart nếu không có láng giềng nào
                current = self._random_restart(current)
                path.append(current)
                visited.add(self._state_to_tuple(current))
                continue
                
            # Chọn ngẫu nhiên trong các láng giềng
            next_state = self._select_next_state(current, neighbors, temperature)
            
            # Cập nhật trạng thái tốt nhất tìm thấy
            current_h = self.heuristic(current)
            if current_h < best_h:
                best_state = current
                best_h = current_h
            
            # Di chuyển đến trạng thái mới (có thể chấp nhận trạng thái xấu hơn)
            current = next_state
            path.append(current)
            visited.add(self._state_to_tuple(current))
            
            # Giảm nhiệt độ (Simulated Annealing)
            temperature *= cooling_rate
            
        return None if best_h > 0 else path  # Trả về kết quả nếu tìm thấy goal

    def _get_unvisited_neighbors(self, state, visited):
        neighbors = []
        blank = find_blank(state)
        
        for dx, dy in directions:
            nx, ny = blank[0] + dx, blank[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                new_state = swap_tiles(state, *blank, nx, ny)
                state_tuple = self._state_to_tuple(new_state)
                if state_tuple not in visited:
                    neighbors.append(new_state)
        
        return neighbors

    def _select_next_state(self, current, neighbors, temperature):

        current_h = self.heuristic(current)
        candidates = []
        
        for neighbor in neighbors:
            neighbor_h = self.heuristic(neighbor)
            delta = current_h - neighbor_h
            
            if delta > 0:  # Neighbor tốt hơn
                candidates.append((neighbor, 1.0))  # Luôn chấp nhận
            else:  # Neighbor xấu hơn
                # Tính xác suất chấp nhận theo Simulated Annealing
                probability = exp(delta / (temperature + 1e-10))
                candidates.append((neighbor, probability))
        
        # Chọn ngẫu nhiên theo trọng số xác suất
        states, probabilities = zip(*candidates)
        next_state = random.choices(states, weights=probabilities, k=1)[0]
        return next_state

    def _random_restart(self, state, steps=20):
        current = [row[:] for row in state]
        for _ in range(steps):
            blank = find_blank(current)
            possible_moves = []
            for dx, dy in directions:
                nx, ny = blank[0] + dx, blank[1] + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    possible_moves.append((dx, dy))
            
            if possible_moves:
                dx, dy = random.choice(possible_moves)
                nx, ny = blank[0] + dx, blank[1] + dy
                current = swap_tiles(current, *blank, nx, ny)
        return current

    def _state_to_tuple(self, state):
        return tuple(tuple(row) for row in state)
class IDAStarSolver(HeuristicSolver):
    def solve(self, start, goal):
        bound = self.heuristic(start)
        path = [start]
        while True:
            t = self._search(path, 0, bound)
            if t == "FOUND":
                return path
            if t == float('inf'):
                return None
            bound = t

    def _search(self, path, g, bound):
        state = path[-1]
        f = g + self.heuristic(state)
        if f > bound:
            return f
        if state == goal_state:
            return "FOUND"
        min_cost = float('inf')
        blank = find_blank(state)
        for dx, dy in directions:
            nx, ny = blank[0] + dx, blank[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                new_state = swap_tiles(state, *blank, nx, ny)
                if new_state not in path:
                    path.append(new_state)
                    t = self._search(path, g + 1, bound)
                    if t == "FOUND":
                        return "FOUND"
                    if t < min_cost:
                        min_cost = t
                    path.pop()
        return min_cost


class SteepestHillClimbingSolver(HeuristicSolver):
    def solve(self, start, goal, max_attempts=100):

        current = deepcopy(start)
        path = [deepcopy(current)]
        visited = set([self._state_to_tuple(current)])
        attempts = 0
        
        while attempts < max_attempts:
            if self._state_to_tuple(current) == self._state_to_tuple(goal):
                return path
                
            neighbors = self._get_unvisited_neighbors(current, visited)
            if not neighbors:
                break
                
            current_h = self.heuristic(current)
            best_neighbor, best_h = self._find_best_neighbor(neighbors)
            
            if best_h < current_h:
                current = best_neighbor
                path.append(deepcopy(current))
                visited.add(self._state_to_tuple(current))
                attempts = 0  # Reset counter khi có tiến bộ
            else:
                # Chọn ngẫu nhiên nếu không cải thiện
                current = random.choice(neighbors)
                path.append(deepcopy(current))
                visited.add(self._state_to_tuple(current))
                attempts += 1
        print(f"Reached max attempts ({max_attempts}) without finding solution!")
        return path if self._state_to_tuple(current) == self._state_to_tuple(goal) else None

    def _get_unvisited_neighbors(self, state, visited):
        neighbors = []
        blank = find_blank(state)
        
        for dx, dy in directions:
            nx, ny = blank[0] + dx, blank[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                new_state = swap_tiles(deepcopy(state), blank[0], blank[1], nx, ny)
                state_tuple = self._state_to_tuple(new_state)
                if state_tuple not in visited:
                    neighbors.append(new_state)
        
        return neighbors

    def _find_best_neighbor(self, neighbors):
        best_h = float('inf')
        best_neighbor = None
        
        for neighbor in neighbors:
            h = self.heuristic(neighbor)
            if h < best_h:
                best_h = h
                best_neighbor = neighbor
                
        return best_neighbor, best_h

    def _state_to_tuple(self, state):
        return tuple(tuple(row) for row in state)
import heapq
import random
from collections import deque
from copy import deepcopy

class NondeterministicSolver(PuzzleSolver):
    def __init__(self, success_prob=0.8):

        self.success_prob = success_prob

    def solve(self, start, goal):

        # Convert to tuple for hashable states
        start_tuple = tuple(tuple(row) for row in start)
        goal_tuple = tuple(tuple(row) for row in goal)
        
        # Priority queue: (estimated_total_cost, actual_cost, state, path)
        heap = []
        heapq.heappush(heap, (self.expected_heuristic(start, goal), 0, start_tuple, [start_tuple]))
        
        visited = set()
        
        while heap:
            _, cost, state, path = heapq.heappop(heap)
            
            if state == goal_tuple:
                # Convert back to list format
                return [[list(row) for row in s] for s in path]
                
            if state in visited:
                continue
            visited.add(state)
            
            # Get all possible next states with probabilities
            neighbors = self.get_neighbors(state)
            
            for next_state, prob in neighbors:
                if next_state not in visited:
                    new_cost = cost + 1  # Each move costs 1
                    # Adjust heuristic by probability
                    heuristic = self.expected_heuristic(next_state, goal) / prob
                    heapq.heappush(heap, (new_cost + heuristic, new_cost, next_state, path + [next_state]))
        
        return None

    def get_neighbors(self, state):

        blank = self.find_blank(state)
        if blank is None:
            return []
            
        possible_moves = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = blank[0] + dx, blank[1] + dy
            if 0 <= nx < len(state) and 0 <= ny < len(state[0]):
                possible_moves.append((dx, dy))
        
        neighbors = []
        for dx, dy in possible_moves:
            # Intended move
            intended_state = self.swap_tiles(state, blank[0], blank[1], blank[0]+dx, blank[1]+dy)
            neighbors.append((intended_state, self.success_prob))
            
            # Unintended moves
            remaining_prob = (1 - self.success_prob) / max(1, len(possible_moves)-1)
            for other_dx, other_dy in possible_moves:
                if (other_dx, other_dy) != (dx, dy):
                    unintended_state = self.swap_tiles(state, blank[0], blank[1], blank[0]+other_dx, blank[1]+other_dy)
                    neighbors.append((unintended_state, remaining_prob))
        
        return neighbors

    def expected_heuristic(self, state, goal):
        distance = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                val = state[i][j]
                if val != 0:  # Skip blank
                    goal_i, goal_j = self.find_position(goal, val)
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def find_blank(self, state):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    return (i, j)
        return None

    def find_position(self, state, value):
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == value:
                    return (i, j)
        return (-1, -1)

    def swap_tiles(self, state, i1, j1, i2, j2):
        state = [list(row) for row in state]  # Convert to list
        new_state = [row[:] for row in state]
        new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
        return tuple(tuple(row) for row in new_state)

class PartialObservationSolver(PuzzleSolver):
    def __init__(self, visible_radius=1, num_hidden=3):
        self.visible_radius = visible_radius  # How many tiles around blank are visible
        self.num_hidden = num_hidden        # How many random tiles are hidden
        self.hidden_tiles = set()            # Positions of hidden tiles

    def solve(self, start, goal):
        # Convert start to list of lists if it's a tuple
        if isinstance(start, tuple):
            start = [list(row) for row in start]
        if isinstance(goal, tuple):
            goal = [list(row) for row in goal]
            
        # Mark random tiles as hidden (except the blank)
        blank_pos = self.find_blank(start)
        all_tiles = [(i,j) for i in range(len(start)) 
                     for j in range(len(start[0])) if (i,j) != blank_pos]
        self.hidden_tiles = set(random.sample(all_tiles, min(self.num_hidden, len(all_tiles))))
        
        queue = deque([(start, [])])
        visited = set()
        
        while queue:
            state, path = queue.popleft()
            
            # Check if visible parts match the goal
            if self.visible_matches(state, goal):
                return path + [state]
            
            # Get blank position
            blank = self.find_blank(state)
            if blank is None:
                continue
                
            # Try moving blank in all directions
            for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                ni, nj = blank[0]+di, blank[1]+dj
                if 0 <= ni < len(state) and 0 <= nj < len(state[0]):
                    # Create a deep copy of the state
                    new_state = [row[:] for row in state]
                    # Perform the swap
                    new_state[blank[0]][blank[1]], new_state[ni][nj] = new_state[ni][nj], new_state[blank[0]][blank[1]]
                    
                    # Reveal tile if blank moves to a hidden position
                    if (ni, nj) in self.hidden_tiles:
                        self.hidden_tiles.remove((ni, nj))
                    
                    # Convert to tuple for visited check
                    state_tuple = tuple(tuple(row) for row in new_state)
                    if state_tuple not in visited:
                        visited.add(state_tuple)
                        queue.append((new_state, path + [new_state]))
        
        return None

    def visible_matches(self, state, goal):
        # Handle case where state is a tuple
        if isinstance(state, tuple):
            state = [list(row) for row in state]
        if isinstance(goal, tuple):
            goal = [list(row) for row in goal]
            
        blank = self.find_blank(state)
        
        # Check tiles around blank
        if blank:
            for i in range(max(0, blank[0]-self.visible_radius), min(len(state), blank[0]+self.visible_radius+1)):
                for j in range(max(0, blank[1]-self.visible_radius), min(len(state[0]), blank[1]+self.visible_radius+1)):
                    if state[i][j] != goal[i][j]:
                        return False
        
        # Check non-hidden tiles
        for i in range(len(state)):
            for j in range(len(state[0])):
                if (i,j) not in self.hidden_tiles and state[i][j] != goal[i][j]:
                    return False
        return True

    def find_blank(self, state):
        # Handle case where state is a tuple
        if isinstance(state, tuple):
            state = [list(row) for row in state]
            
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    return (i, j)
        return None
class BeliefStateSolver(PuzzleSolver):
    def solve(self, start, goal):
        initial_belief = frozenset([start])
        goal_state = goal
        queue = deque([(initial_belief, [])])
        visited = set()
        visited.add(initial_belief)
        actions = directions  # Các hướng di chuyển

        while queue:
            current_belief, path = queue.popleft()
            
            # Kiểm tra tất cả trạng thái đều là goal
            if all(state == goal_state for state in current_belief):
                return path  # Trả về chuỗi hành động
            
            for action in actions:
                next_belief = set()
                for state in current_belief:
                    i, j = find_blank(state)
                    di, dj = action
                    new_i, new_j = i + di, j + dj
                    
                    if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                        new_state = swap_tiles(state, i, j, new_i, new_j)
                    else:
                        new_state = state  # Giữ nguyên nếu không di chuyển được
                    next_belief.add(new_state)
                
                next_belief_frozen = frozenset(next_belief)
                if next_belief_frozen not in visited:
                    visited.add(next_belief_frozen)
                    queue.append((next_belief_frozen, path + [action]))
        
        return None  # Không tìm thấy giải pháp
class NoObservationSolver(PuzzleSolver):
    def __init__(self, max_states=1):  # Giảm max_states xuống 20
        self.max_states = max_states
        self.visited = set()

    def is_solvable(self, state):
        flat = [tile for row in state for tile in row if tile != 0]
        inv_count = sum(1 for i in range(len(flat)) for j in range(i+1, len(flat)) if flat[i] > flat[j])
        return inv_count % 2 == 0

    def generate_random_belief_states(self):
        from itertools import permutations
        import random

        perms = list(permutations(range(9)))
        random.shuffle(perms)

        states = set()
        for perm in perms:
            matrix = tuple(tuple(perm[i*3:(i+1)*3]) for i in range(3))
            if self.is_solvable(matrix):
                states.add(matrix)
                if len(states) >= self.max_states:
                    break
        return list(states)

    def apply_action(self, state, direction):
        i, j = find_blank(state)
        ni, nj = i + direction[0], j + direction[1]
        if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
            return swap_tiles(state, i, j, ni, nj)
        return state

    def solve(self, start, goal):
        belief = self.generate_random_belief_states()
        if not belief:
            print("Không thể tạo đủ belief states hợp lệ.")
            return None

        queue = deque()
        queue.append((belief, []))

        while queue:
            belief, actions = queue.popleft()

            if all(state == goal for state in belief):
                return [goal]

            for direction in directions:
                next_belief = set()
                for state in belief:
                    next_state = self.apply_action(state, direction)
                    next_belief.add(next_state)

                if len(next_belief) > self.max_states:
                    continue

                key = frozenset(next_belief)
                if key in self.visited:
                    continue
                self.visited.add(key)

                queue.append((list(next_belief), actions + [direction]))

        print("Không tìm thấy lời giải trong giới hạn.")
        return None
class QLearningSolver(PuzzleSolver):
    def __init__(self, alpha=0.8, gamma=0.9, epsilon=0.1, episodes=2000):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.episodes = episodes  # Number of episodes to run Q-learning
        self.q_table = {}  # Dictionary to store Q-values
        
    def get_actions(self, state):
        # Trả về tất cả các hành động có thể từ trạng thái hiện tại (di chuyển các ô)
        actions = []
        blank_row, blank_col = find_blank(state)
        for direction in directions:
            new_row, new_col = blank_row + direction[0], blank_col + direction[1]
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                actions.append((blank_row, blank_col, new_row, new_col))
        return actions

    def update_q_table(self, state, action, reward, next_state):
        # Cập nhật bảng Q theo công thức Q-learning
        max_q_next = max(self.q_table.get(next_state, {}).values(), default=0)
        current_q = self.q_table.get(state, {}).get(action, 0)
        self.q_table.setdefault(state, {})[action] = current_q + self.alpha * (reward + self.gamma * max_q_next - current_q)

    def choose_action(self, state):
        # Lựa chọn hành động theo chiến lược epsilon-greedy
        if random.random() < self.epsilon:
            # Khám phá (explore)
            actions = self.get_actions(state)
            return random.choice(actions)
        else:
            # Tận dụng (exploit)
            if state not in self.q_table:
                return random.choice(self.get_actions(state))
            max_q_action = max(self.q_table[state], key=self.q_table[state].get)
            return max_q_action
    
    def solve(self, start, goal):
        for episode in range(self.episodes):
            state = start
            total_reward = 0
            while state != goal:
                action = self.choose_action(state)
                next_state = swap_tiles(state, *action)
                reward = -1 if next_state != goal else 100  # Phần thưởng tiêu cực khi không phải trạng thái mục tiêu
                self.update_q_table(state, action, reward, next_state)
                state = next_state
                total_reward += reward
            print(f"Episode {episode + 1}: Total Reward: {total_reward}")
        
        # Trả về chuỗi hành động tối ưu từ trạng thái ban đầu
        state = start
        path = [state]
        while state != goal:
            action = self.choose_action(state)
            next_state = swap_tiles(state, *action)
            path.append(next_state)
            state = next_state
        return path
#region [Giao diện người dùng]
class Button:
    def __init__(self, text, pos, action, color):
        self.text = text
        self.rect = pygame.Rect(pos[0], pos[1], BUTTON_SIZE, 50)
        self.action = action
        self.color = color
        self.hover = False

    def draw(self, surface):
        current_color = [min(255, c + 40) if self.hover else c for c in self.color]
        pygame.draw.rect(surface, current_color, self.rect, border_radius=5)
        font = pygame.font.Font(None, 30)
        text = font.render(self.text, True, COLORS["text"])
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

class PuzzleUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("8-Puzzle Solver Pro")
        
        self.algorithms = {
            "BFS": BFSSolver(),
            "DFS": DFSSolver(),
            "UCS": UCSolver(),
            "A*": AStarSolver(),
            "IDA*": IDAStarSolver(),
            "Greedy": GreedySolver(),
            "SIMPLE": HillClimbingSolver(),
            "STEEPH": SteepestHillClimbingSolver(),
            "STOCH": StochasticHillClimbingSolver(),
            "Beam": BeamSearchSolver(beam_width=2),
            "SA": SimulatedAnnealingSolver(),
            "Genetic": GeneticSolver(),
            "IDDFS": IDDFSSolver(),
            "Nondeterministic": NondeterministicSolver(),  
            "PartialObservation": PartialObservationSolver(),
            "NoObservation": NoObservationSolver(),
            "Q-Learning": QLearningSolver(),

        }
        
        self.buttons = self.create_buttons()
        self.path = deque()
        self.current_step = 0
        self.start_state = ((2, 6, 5), (8, 0, 7), (4, 3, 1))  # Trạng thái ban đầu cũ
        self.end_state = self.start_state
        self.steps_display = None  # Hiển thị số bước
        self.time_display = None  # Hiển thị thời gian

    def create_buttons(self):
        return [
              # Nút tạo trạng thái mới

            # Hàng 1
            Button("BFS", (10, 500), "BFS",(241, 76, 76)),
            Button("DFS", (BUTTON_SIZE+20, 500), "DFS",(241, 76, 76)),
            Button("UCS", (2*BUTTON_SIZE+30, 500), "UCS",(241, 76, 76)),
            Button("IDDFS", (3*BUTTON_SIZE+40, 500), "IDDFS", (241, 76, 76)),
            # Hàng 2
            Button("IDA*", (10, 560), "IDA*", (0, 255, 127)),
            Button("A*", (BUTTON_SIZE+20, 560), "A*", (0, 255, 127)),
            Button("Greedy", (2*BUTTON_SIZE+30, 560), "Greedy", (0, 255, 127)),
            Button("Beam", (5*BUTTON_SIZE+60, 620), "Beam", (200, 120, 200)),
            Button("Genetic", (4*BUTTON_SIZE+50, 620), "Genetic", (200, 120, 200)),

            # Hàng 3
            Button("STOCH", (10, 620), "STOCH", (200, 120, 200)),
            Button("STEEPH", (BUTTON_SIZE+20, 620), "STEEPH", (200, 120, 200)),
            Button("SA", (2*BUTTON_SIZE+30, 620), "SA", (200, 120, 200)),
            Button("SIMPLE", (3*BUTTON_SIZE+40, 620), "SIMPLE", (200, 120, 200)),
            Button("New w/ FC", (4*BUTTON_SIZE+50, 560), "FORWARD_CHECK", (0, 0, 102)),


            # Hàng 4
            Button("NO OBS", (10, 680), "NoObservation", (110, 15, 10)),
            Button("SWNA", (BUTTON_SIZE+20, 680), "Nondeterministic",(110, 15, 10)),
            Button("PO", (2*BUTTON_SIZE+30, 680), "PartialObservation", (110, 15, 10)),
            Button("Q-LEARN", (3*BUTTON_SIZE+40, 680), "Q-Learning", (255, 153, 0)),
            Button("New w/ BT", (3*BUTTON_SIZE+40, 560), "GENERATE_START_STATE", (0, 0, 102)),
            Button("New w/ MIN", (5*BUTTON_SIZE+60, 560), "GENERATE_MIN_CONFLICT", (0, 0, 102)),

            
        ]
    def draw_grid(self, state, position=(0, 0)):
        font = pygame.font.Font(None, FONT_SIZE)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = state[i][j]
                rect = pygame.Rect(position[0] + j * TILE_SIZE, position[1] + i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                color = COLORS["tile"] if value != 0 else (200, 200, 200)
                pygame.draw.rect(self.screen, color, rect, border_radius=5)
                if value != 0:
                    text = font.render(str(value), True, COLORS["text"])
                    self.screen.blit(text, (rect.x + TILE_SIZE//3, rect.y + TILE_SIZE//4))

    def run(self):
        running = True
        while running:
            self.screen.fill(COLORS["background"])
            
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                btn.hover = btn.rect.collidepoint(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.update_display()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # Cập nhật UI để xử lý hành động
    def handle_click(self, pos):
        for btn in self.buttons:
            if btn.rect.collidepoint(pos):
                if btn.text == "New w/ BT":
                    self.start_state = generate_start_state_by_csp()
                    self.end_state = self.start_state
                    self.path = None
                    self.current_step = 0
                    self.steps_display = None
                    self.time_display = None
                    print(f"New start state: {self.start_state}")
                elif btn.text == "New w/ MIN":
                    self.start_state = generate_start_state_by_min_conflict()
                    self.end_state = self.start_state
                    self.path = None
                    self.current_step = 0
                    self.steps_display = None
                    self.time_display = None
                    print(f"New start state: {self.start_state}")
                elif btn.text == "New w/ FC":
                    self.start_state = generate_start_state_with_forward_checking()
                    self.end_state = self.start_state
                    self.path = None
                    self.current_step = 0
                    self.steps_display = None
                    self.time_display = None
                    print(f"New FC start state: {self.start_state}")
                else:
                    self.end_state = self.start_state
                    self.path = None
                    self.current_step = 0
                    self.steps_display = None
                    self.time_display = None

                    solver = self.algorithms.get(btn.action)
                    if solver:
                        start_time = time.time()
                        try:
                            self.path = solver.solve(self.start_state, goal_state)
                            elapsed = round(time.time() - start_time, 2)
                            self.time_display = elapsed

                            if self.path:
                                self.steps_display = len(self.path) - 1
                                self.end_state = goal_state
                            else:
                                self.steps_display = "CAN'T SOLVE!"
                                self.time_display = 0

                        except Exception as e:
                            self.steps_display = f"Lỗi: {str(e)}"
                            self.time_display = 0




    def update_display(self):
        if self.path:
            current_state = self.path.pop(0)
            self.draw_grid(current_state)
            pygame.time.delay(STEP_DELAY)
        else:
            self.draw_grid(self.end_state)

        # Goal State nhỏ
        goal_label_font = pygame.font.Font(None, 28)
        goal_label = goal_label_font.render("Goal", True, COLORS["text"])
        self.screen.blit(goal_label, (WIDTH - 250, 20))
        self.draw_mini_grid(goal_state, position=(WIDTH - 250, 50))

        for btn in self.buttons:
            btn.draw(self.screen)

        font = pygame.font.Font(None, FONT_SIZE)
        if self.steps_display is not None:
            if isinstance(self.steps_display, int):
                steps_text = font.render(f"Step: {self.steps_display}", True, COLORS["text"])
            else:
                steps_text = font.render(self.steps_display, True, COLORS["text"])
            self.screen.blit(steps_text, (WIDTH - 250, 400))

        if self.time_display is not None:
            time_text = font.render(f"Time: {self.time_display}s", True, COLORS["text"])
            self.screen.blit(time_text, (WIDTH - 250, 450))
    def draw_mini_grid(self, state, position=(0, 0), tile_size=70):
        font = pygame.font.Font(None, 24)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = state[i][j]
                rect = pygame.Rect(position[0] + j * tile_size, position[1] + i * tile_size, tile_size, tile_size)
                color = COLORS["tile"] if value != 0 else (200, 200, 200)
                pygame.draw.rect(self.screen, color, rect, border_radius=3)
                if value != 0:
                    text = font.render(str(value), True, COLORS["text"])
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

#endregion

#region [Các hàm tiện ích]
def is_solvable(assignment):
    """Check if the 8-puzzle assignment is solvable."""
    if len(assignment) != 9:
        return False
    
    # Ensure all tiles 0 to 8 appear exactly once
    if sorted(assignment) != list(range(9)):
        return False
    
    # Count inversions (excluding the blank tile 0)
    inversions = 0
    tiles = [x for x in assignment if x != 0]  # Exclude blank
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    
    # Solvable if inversions is even (for goal state with 0 inversions)
    return inversions % 2 == 0

def generate_start_state_with_forward_checking():
    def backtrack(assignment, domains):
        if len(assignment) == 9:
            # Check if the state is valid and solvable
            if is_solvable(assignment):
                return assignment
            return None
        
        # Choose the next unassigned variable (position)
        var = len(assignment)
        
        # Shuffle values to ensure randomness
        values = domains[var].copy()
        random.shuffle(values)
        
        for value in values:
            # Skip if value is already used
            if value in assignment:
                continue

            # Temporarily assign the value
            new_assignment = assignment + [value]

            # Forward checking: remove the assigned value from remaining domains
            new_domains = [d.copy() for d in domains]
            for d in new_domains[var + 1:]:
                if value in d:
                    d.remove(value)

            # Continue if no domain is empty
            if all(len(d) > 0 for d in new_domains[var + 1:]):
                result = backtrack(new_assignment, new_domains)
                if result:
                    return result
        return None

    # Initialize domains: 0 to 8 for each position
    initial_domains = [list(range(9)) for _ in range(9)]
    
    # Generate a state with exactly 9 tiles (0 to 8)
    result = backtrack([], initial_domains)
    
    if result:
        # Convert to 3x3 grid as tuple of tuples
        grid = tuple(tuple(result[i:i + 3]) for i in range(0, 9, 3))
        print("Generated 8-puzzle start state:", grid)
        return grid
    else:
        # Fallback to a simple solvable state
        fallback = ((1, 2, 3), (4, 5, 6), (7, 0, 8))
        print("Using fallback state:", fallback)
        return fallback
    
def generate_start_state_by_min_conflict(max_steps=1000):
    current = list(range(9))
    random.shuffle(current)
    
    def conflicts(state):
        """Tính số ô không ở đúng vị trí"""
        return sum(1 for i, val in enumerate(state) if val != 0 and val != goal_state[i // 3][i % 3])
    
    for step in range(max_steps):
        if is_solvable(current):
            if conflicts(current) <= 2:
                break
        # Chọn 2 ô bất kỳ để swap giảm xung đột
        idx1, idx2 = random.sample(range(9), 2)
        current[idx1], current[idx2] = current[idx2], current[idx1]

    grid = [tuple(current[i:i+3]) for i in range(0, 9, 3)]
    print(f"Min-conflict state after {step+1} steps: {grid}")
    return tuple(grid)

def generate_start_state_by_csp():
    from itertools import permutations
    values = list(range(9))
    
    # Thử các hoán vị ngẫu nhiên đến khi tìm được trạng thái hợp lệ
    attempts = 0
    while True:
        attempts += 1
        candidate = random.sample(values, 9)
        if is_solvable(candidate):
            grid = [tuple(candidate[i:i + 3]) for i in range(0, 9, 3)]
            print(f"Generated after {attempts} attempts: {grid}")
            return tuple(grid)
        # Nếu không hợp lệ, tiếp tục thử
        if attempts >= 100:  # Giới hạn số lần thử để tránh vô hạn
            print("Failed to generate a solvable state after 100 attempts.")
            break
def is_goal_state(state, goal_state):
    """Kiểm tra nếu trạng thái là trạng thái mục tiêu."""
    return state == goal_state

def get_possible_actions(state):
    """Lấy các hành động có thể thực hiện từ trạng thái hiện tại."""
    actions = []
    blank_row, blank_col = find_blank(state)
    
    # Di chuyển ô trống lên, xuống, trái, phải
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        new_row, new_col = blank_row + dr, blank_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            actions.append((new_row, new_col))
    return actions

def find_blank(state):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if state[i][j] == 0:
                return i, j

def swap_tiles(state, i1, j1, i2, j2):
    new_state = [list(row) for row in state]
    new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
    return tuple(tuple(row) for row in new_state)
#endregion

if __name__ == "__main__":
    ui = PuzzleUI()
    ui.run()
