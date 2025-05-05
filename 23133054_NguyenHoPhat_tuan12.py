import pygame
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

start_state = ((2, 6, 5), (8, 0, 7), (4, 3, 1))
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

import random
from copy import deepcopy
from heapq import nsmallest

import random
from copy import deepcopy
from heapq import nsmallest
from collections import defaultdict

import random
from copy import deepcopy

class GeneticSolver(PuzzleSolver):
    def __init__(self, population_size=100, max_generations=100, mutation_rate=0.2, crossover_rate=0.7, tournament_size=5):
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        
    def solve(self, start, goal):
        # Initialize population with random moves from start state
        population = [self.generate_individual(start) for _ in range(self.population_size)]
        
        for generation in range(self.max_generations):
            # Evaluate fitness
            fitness_scores = [self.evaluate_fitness(individual, goal) for individual in population]
            
            # Check if we've found a solution
            best_fitness = min(fitness_scores)
            if best_fitness == 0:
                best_index = fitness_scores.index(best_fitness)
                solution_path = self.extract_solution_path(population[best_index], start)
                if solution_path:
                    return solution_path
            
            # Create new generation
            new_population = []
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self.tournament_selection(population, fitness_scores)
                parent2 = self.tournament_selection(population, fitness_scores)
                
                # Crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = self.crossover(parent1, parent2)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()
                
                # Mutation
                if random.random() < self.mutation_rate:
                    child1 = self.mutate(child1)
                if random.random() < self.mutation_rate:
                    child2 = self.mutate(child2)
                
                new_population.extend([child1, child2])
            
            population = new_population[:self.population_size]
        
        # Return best solution found (if any)
        fitness_scores = [self.evaluate_fitness(individual, goal) for individual in population]
        best_index = fitness_scores.index(min(fitness_scores))
        solution_path = self.extract_solution_path(population[best_index], start)
        return solution_path if solution_path else None
    
    def generate_individual(self, start_state):
        """Generate an individual as a sequence of moves (up to 50 moves)"""
        max_moves = 200
        individual = []
        current_state = start_state
        
        for _ in range(max_moves):
            blank_i, blank_j = find_blank(current_state)
            possible_moves = []
            
            for di, dj in directions:
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                    possible_moves.append((di, dj))
            
            if not possible_moves:
                break
                
            move = random.choice(possible_moves)
            individual.append(move)
            current_state = swap_tiles(current_state, blank_i, blank_j, blank_i + move[0], blank_j + move[1])
            
        return individual
    
    def evaluate_fitness(self, individual, goal_state):
        """Calculate fitness by simulating the moves and checking distance to goal"""
        current_state = start_state
        
        for move in individual:
            blank_i, blank_j = find_blank(current_state)
            new_i, new_j = blank_i + move[0], blank_j + move[1]
            
            if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                current_state = swap_tiles(current_state, blank_i, blank_j, new_i, new_j)
            else:
                # Penalize invalid moves
                return float('inf')
        
        # Use Manhattan distance heuristic
        distance = 0
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = current_state[i][j]
                if value != 0:
                    goal_row = (value - 1) // GRID_SIZE
                    goal_col = (value - 1) % GRID_SIZE
                    distance += abs(i - goal_row) + abs(j - goal_col)
        
        # Also consider path length to prefer shorter solutions
        return distance + len(individual) * 0.1
    
    def tournament_selection(self, population, fitness_scores):
        """Select an individual using tournament selection"""
        tournament = random.sample(list(zip(population, fitness_scores)), self.tournament_size)
        tournament.sort(key=lambda x: x[1])  # Sort by fitness
        return tournament[0][0]  # Return the best in the tournament
    
    def crossover(self, parent1, parent2):
        """Perform ordered crossover between two parents"""
        if len(parent1) < 2 or len(parent2) < 2:
            return parent1.copy(), parent2.copy()
            
        # Select crossover points
        point1 = random.randint(0, min(len(parent1), len(parent2)) - 1)
        point2 = random.randint(point1 + 1, min(len(parent1), len(parent2)))
        
        # Create children
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        
        return child1, child2
    
    def mutate(self, individual):
        """Mutate an individual by changing some moves"""
        if not individual:
            return individual
            
        mutated = individual.copy()
        for i in range(len(mutated)):
            if random.random() < 0.1:  # Chance to mutate each move
                blank_i, blank_j = find_blank(self.simulate_moves(start_state, mutated[:i]))
                possible_moves = []
                
                for di, dj in directions:
                    new_i, new_j = blank_i + di, blank_j + dj
                    if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                        possible_moves.append((di, dj))
                
                if possible_moves:
                    mutated[i] = random.choice(possible_moves)
        
        return mutated
    
    def simulate_moves(self, start_state, moves):
        """Simulate a sequence of moves from a starting state"""
        current_state = start_state
        for move in moves:
            blank_i, blank_j = find_blank(current_state)
            new_i, new_j = blank_i + move[0], blank_j + move[1]
            if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                current_state = swap_tiles(current_state, blank_i, blank_j, new_i, new_j)
        return current_state
    
    def extract_solution_path(self, individual, start_state):
        """Convert an individual to a valid solution path"""
        path = [start_state]
        current_state = start_state
        
        for move in individual:
            blank_i, blank_j = find_blank(current_state)
            new_i, new_j = blank_i + move[0], blank_j + move[1]
            
            if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                current_state = swap_tiles(current_state, blank_i, blank_j, new_i, new_j)
                path.append(current_state)
            else:
                return None  # Invalid move sequence
            
            if current_state == goal_state:
                return path
        
        return None if current_state != goal_state else path
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
        """
        Phiên bản cải tiến của IDDFS với:
        1. Theo dõi các trạng thái đã xét để tránh lặp
        2. Tối ưu bộ nhớ bằng cách sử dụng tuple cho visited set
        3. Kiểm tra goal state ngay khi tìm thấy
        4. Hỗ trợ tìm kiếm theo chiều sâu tăng dần hiệu quả
        """
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
        """Chuyển state sang dạng tuple có thể hash được"""
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
import random
import math
from copy import deepcopy

class SimulatedAnnealingSolver(HeuristicSolver):
    def solve(self, start, goal, initial_temp=1000, cooling_rate=0.995, max_steps=10000):
        """
        Improved Simulated Annealing implementation with:
        1. Better memory management (limited visited states tracking)
        2. Smarter stopping criteria
        3. Adaptive neighbor selection
        4. Path reconstruction optimization
        """
        current_state = start
        best_state = start
        best_h = self.heuristic(start)
        current_h = best_h
        path = [start]  # Only store key states to save memory
        
        # Use limited-size set for visited states to prevent memory explosion
        visited = set()
        visited.add(self._state_to_tuple(start))
        
        T = initial_temp
        no_improvement_steps = 0
        max_no_improvement = 500  # Stop if no improvement for this many steps
        
        for step in range(max_steps):
            if current_state == goal:
                return self._reconstruct_path(path, start, current_state)
            
            # Get all possible neighbors first
            neighbors = self._get_all_neighbors(current_state)
            
            # Filter out recently visited states (but not all to allow some revisiting)
            unvisited_neighbors = [n for n in neighbors 
                                 if self._state_to_tuple(n) not in visited or random.random() < 0.1]
            
            # If no unvisited neighbors, select from all neighbors
            if not unvisited_neighbors:
                next_state = random.choice(neighbors)
            else:
                # Prefer neighbors with better heuristic
                neighbors_sorted = sorted(unvisited_neighbors, key=lambda x: self.heuristic(x))
                next_state = neighbors_sorted[0] if random.random() < 0.7 else random.choice(neighbors_sorted[:3])
            
            next_h = self.heuristic(next_state)
            delta_e = next_h - current_h
            
            # Acceptance criteria
            if delta_e < 0 or math.exp(-delta_e / max(T, 1e-10)) > random.random():
                current_state = next_state
                current_h = next_h
                
                # Store only every N states to save memory
                if step % 10 == 0 or next_h < best_h:
                    path.append(current_state)
                
                visited.add(self._state_to_tuple(current_state))
                
                # Update best state found
                if next_h < best_h:
                    best_state = current_state
                    best_h = next_h
                    no_improvement_steps = 0
                else:
                    no_improvement_steps += 1
            else:
                no_improvement_steps += 1
            
            # Cooling schedule
            T *= cooling_rate
            
            # Early termination conditions
            if best_h == 0:  # Found solution
                return self._reconstruct_path(path, start, best_state)
            if no_improvement_steps >= max_no_improvement:
                break
            if T < 1e-10 and best_h <= 2:  # Close to solution
                # Try to complete the solution with greedy moves
                final_path = self._complete_with_greedy(best_state, goal)
                if final_path:
                    return self._reconstruct_path(path, start, best_state) + final_path[1:]
                break
        
        # Try to return the best path found
        if best_state == goal:
            return self._reconstruct_path(path, start, best_state)
        
        # Final attempt with greedy approach from best state found
        final_path = self._complete_with_greedy(best_state, goal)
        if final_path:
            return self._reconstruct_path(path, start, best_state) + final_path[1:]
        
        return None

    def _get_all_neighbors(self, state):
        """Generate all possible next states from current state"""
        blank_i, blank_j = find_blank(state)
        neighbors = []
        
        for di, dj in directions:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < GRID_SIZE and 0 <= new_j < GRID_SIZE:
                neighbors.append(swap_tiles(state, blank_i, blank_j, new_i, new_j))
        
        return neighbors

    def _state_to_tuple(self, state):
        """Convert state to hashable tuple"""
        return tuple(tuple(row) for row in state)

    def _reconstruct_path(self, sparse_path, start, end):
        """Reconstruct complete path from sparse state storage"""
        if not sparse_path:
            return [start]
        
        # If end state is already in the path, return up to that point
        for i, state in enumerate(sparse_path):
            if state == end:
                return sparse_path[:i+1]
        
        # Otherwise find the closest state and build path to end
        closest_state = sparse_path[-1]
        path_to_end = self._build_path_between(closest_state, end)
        return sparse_path + path_to_end[1:]

    def _build_path_between(self, start, end):
        """Build path between two states using simple BFS"""
        if start == end:
            return [start]
        
        queue = deque()
        queue.append((start, [start]))
        visited = set()
        visited.add(self._state_to_tuple(start))
        
        while queue:
            current, path = queue.popleft()
            
            for neighbor in self._get_all_neighbors(current):
                if neighbor == end:
                    return path + [neighbor]
                
                neighbor_tuple = self._state_to_tuple(neighbor)
                if neighbor_tuple not in visited:
                    visited.add(neighbor_tuple)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

    def _complete_with_greedy(self, state, goal):
        """Complete the path to goal using greedy best-first search"""
        current = state
        path = [current]
        visited = set()
        visited.add(self._state_to_tuple(current))
        
        while current != goal:
            neighbors = self._get_all_neighbors(current)
            if not neighbors:
                return None
                
            # Choose neighbor with best heuristic
            neighbors.sort(key=lambda x: self.heuristic(x))
            for neighbor in neighbors:
                if self._state_to_tuple(neighbor) not in visited:
                    current = neighbor
                    path.append(current)
                    visited.add(self._state_to_tuple(current))
                    break
            else:
                return None  # No unvisited neighbors
        
        return path

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
        """
        Phiên bản cải tiến của Stochastic Hill Climbing với:
        - Simulated Annealing (giảm nhiệt độ dần)
        - Theo dõi các trạng thái đã xét
        - Random restart khi bị kẹt
        """
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
        """Tạo danh sách các trạng thái kề chưa được xét"""
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
        """
        Chọn trạng thái tiếp theo với xác suất phụ thuộc vào:
        - Độ chênh lệch heuristic
        - Nhiệt độ hiện tại
        """
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
        """Tạo trạng thái ngẫu nhiên bằng cách thực hiện nhiều bước di chuyển ngẫu nhiên"""
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
        """Chuyển state sang dạng tuple có thể hash được"""
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

import random

import random
from copy import deepcopy

import random
from copy import deepcopy

class SteepestHillClimbingSolver(HeuristicSolver):
    def solve(self, start, goal, max_attempts=100):
        """
        Phiên bản cải tiến của Steepest Ascent Hill Climbing với:
        1. Theo dõi các trạng thái đã xét
        2. Hỗ trợ random restart khi bị kẹt
        3. Quản lý bộ nhớ hiệu quả
        4. Tối ưu hóa tìm kiếm láng giềng
        """
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
        """Tạo danh sách các trạng thái kề chưa được xét"""
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
        """Tìm trạng thái láng giềng tốt nhất"""
        best_h = float('inf')
        best_neighbor = None
        
        for neighbor in neighbors:
            h = self.heuristic(neighbor)
            if h < best_h:
                best_h = h
                best_neighbor = neighbor
                
        return best_neighbor, best_h

    def _state_to_tuple(self, state):
        """Chuyển state sang dạng tuple có thể hash được"""
        return tuple(tuple(row) for row in state)
import heapq
import random
from collections import deque
from copy import deepcopy

class NondeterministicSolver(PuzzleSolver):
    def __init__(self, success_prob=0.8):
        """
        Solver that accounts for non-deterministic actions with success probability
        
        Args:
            success_prob: Probability that the intended move succeeds (default 0.8)
        """
        self.success_prob = success_prob

    def solve(self, start, goal):
        """
        Solves the puzzle using probabilistic actions
        
        Args:
            start: Initial puzzle state
            goal: Target puzzle state
            
        Returns:
            Solution path if found, None otherwise
        """
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
        """
        Get possible next states with their probabilities
        
        Args:
            state: Current puzzle state
            
        Returns:
            List of (next_state, probability) tuples
        """
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
        """Expected Manhattan distance heuristic"""
        distance = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                val = state[i][j]
                if val != 0:  # Skip blank
                    goal_i, goal_j = self.find_position(goal, val)
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance

    def find_blank(self, state):
        """Find blank position (0)"""
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    return (i, j)
        return None

    def find_position(self, state, value):
        """Find position of a value in the state"""
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == value:
                    return (i, j)
        return (-1, -1)

    def swap_tiles(self, state, i1, j1, i2, j2):
        """Swap two tiles and return new state"""
        state = [list(row) for row in state]  # Convert to list
        new_state = [row[:] for row in state]
        new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
        return tuple(tuple(row) for row in new_state)
from collections import deque
from copy import deepcopy

import random
from typing import List, Tuple, Dict, Set, Optional

from collections import deque
import random

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
        """Check if all visible tiles match the goal"""
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
        """Find the position of the blank tile (0)"""
        # Handle case where state is a tuple
        if isinstance(state, tuple):
            state = [list(row) for row in state]
            
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    return (i, j)
        return None
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
        }
        
        self.buttons = self.create_buttons()
        self.path = deque()
        self.current_step = 0
        self.end_state = start_state

    def create_buttons(self):
        return [
            # Hàng 1
            Button("BFS", (10, 500), "BFS", COLORS["button"]["BFS"]),
            Button("DFS", (BUTTON_SIZE+20, 500), "DFS", COLORS["button"]["default"]),
            Button("UCS", (2*BUTTON_SIZE+30, 500), "UCS", COLORS["button"]["UCS"]),
            Button("IDDFS", (3*BUTTON_SIZE+40, 500), "IDDFS", COLORS["button"]["IDDFS"]),
            Button("Genetic", (5*BUTTON_SIZE+60, 500), "Genetic", COLORS["button"]["Genetic"]),
            # Hàng 2
            Button("IDA*", (10, 560), "IDA*", COLORS["button"]["IDA*"]),
            Button("A*", (BUTTON_SIZE+20, 560), "A*", COLORS["button"]["A*"]),
            Button("Greedy", (2*BUTTON_SIZE+30, 560), "Greedy", COLORS["button"]["Greedy"]),
            Button("Beam", (3*BUTTON_SIZE+40, 560), "Beam", COLORS["button"]["Beam"]),
            
            # Hàng 3
            Button("STOCH", (10, 620), "STOCH", (200, 120, 200)),
            Button("STEEPH", (BUTTON_SIZE+20, 620), "STEEPH", COLORS["button"]["Steepest"]),

            Button("SA", (2*BUTTON_SIZE+30, 620), "SA", COLORS["button"]["SA"]),
            Button("SIMPLE", (3*BUTTON_SIZE+40, 620), "SIMPLE", COLORS["button"]["Hill"]),

            # Hàng 4
            Button("IDDFS", (10, 680), "IDDFS", COLORS["button"]["IDDFS"]),
            Button("SWNA", (BUTTON_SIZE+20, 680), "Nondeterministic", COLORS["button"]["Greedy"]),
            Button("PO", (2*BUTTON_SIZE+30, 680), "PartialObservation", COLORS["button"]["Hill"]),
        ]
    def draw_grid(self, state):
        font = pygame.font.Font(None, FONT_SIZE)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = state[i][j]
                rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                color = COLORS["tile"] if value !=0 else (200, 200, 200)
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

    def handle_click(self, pos):
        for btn in self.buttons:
            if btn.rect.collidepoint(pos):
                self.end_state = start_state
                self.path = None
                self.current_step = 0
                try:
                    solver = self.algorithms.get(btn.action)                    
                    if solver:
                        self.path = solver.solve(start_state, goal_state)
                        if not self.path:
                            print(f"{btn.action} không tìm thấy lời giải!")
                        else :
                            print(len(self.path) -1)
                            self.end_state = goal_state
                except Exception as e:
                    print(f"Lỗi: {str(e)}")
    
    def update_display(self):
        if self.path:
            current_state = self.path.pop(0)  # Lấy và xóa state đầu tiên
            self.draw_grid(current_state)
            pygame.time.delay(STEP_DELAY)

        else:
            self.draw_grid(self.end_state)

        for btn in self.buttons:
            btn.draw(self.screen)
#endregion

#region [Các hàm tiện ích]
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