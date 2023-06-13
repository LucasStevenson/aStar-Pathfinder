import pygame
import random
import heapq

# Constants
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
CELL_SIZE = 20 # size of each cell on the grid
NUM_ROWS = WINDOW_WIDTH // CELL_SIZE
NUM_COLS = WINDOW_HEIGHT // CELL_SIZE

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# init pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

class Robot:
    def __init__(self, x, y):
        # x: x coord of robot
        # y: y coord of robot
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        # draws the robot on the grid
        pygame.draw.rect(screen, BLUE, pygame.Rect(self.x*CELL_SIZE, self.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)) # (surface, color, rect)


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        # draws the obstacle on the grid
        # Rect -> (left, top, width, height)
        pygame.draw.rect(screen, BLACK, pygame.Rect(self.x*CELL_SIZE, self.y*CELL_SIZE, CELL_SIZE, CELL_SIZE)) # (surface, color, rect)

def generate_obstacles(num_obstacles):
    """Generates (x,y) coordinate of each obstacle
    Params:
        num_obstacles: number of obstacles to generate
    Returns:
        List of all Obstacle objects
    """
    obstacles = []
    for _ in range(num_obstacles):
        # randomly generate the positions of each obstacle
        # obstacle can be generated anywhere within the grid
        # subtract 1 from numRows and numCols because randint() is inclusive
        x = random.randint(0, NUM_ROWS - 1)
        y = random.randint(0, NUM_COLS - 1)
        # append coord of obstacle into obstacles list
        obstacles.append(Obstacle(x, y))
    return obstacles

def draw_grid():
    """Draws the lines/squares for the grid
    Returns:
        Nothing. Just draws the lines
    """
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW_WIDTH, y))


def is_collision(coord, obstacles):
    """Detects if (x,y) coord collides with an obstacle
    Params:
        coord:     (x,y) coordinate
        obstacles: List of Obstacle objects
    Returns:
        Boolean
    """
    for obstacle in obstacles:
        if coord == (obstacle.x, obstacle.y):
            # then x,y coords of robot is an obstacle and it is a collision
            return True
    # if we made it to this point, then x,y coords is not an obstacle
    # and therefore there is no collision
    return False


def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def aStar(start, end, obstacles):
    """finds the shortest path from `start` point to `end` point using A* algorithm
    Params:
        start:     (x,y) coordinate of starting point
        end:       (x,y) coordinate of ending point
        obstacles: List of Obstacle objects
    Returns:
        Shortest path represented as a list if path exists, otherwise None
    """
    # how does the A* algorithm work?
    # f(x) = g(x) + h(x)
    # g(x): distance from starting point
    # h(x): estimated distance from ending point (manhattan distance)
    # The point of h(x) is to prioritize nodes that are approximately on the right track to the end cell
    # We still use g(x) to determine whether or not we need to update a vertex
    # Basically, A* works exactly like Dijkstra, except theres an added heuristic that reduces the number of vertices we check 
    pq = [(0, start)]
    g_costs = { start: 0 }
    f_costs = {}
    parents = {}
    while pq:
        _, coord = heapq.heappop(pq) # f_cost, (x,y) coord
        x, y = coord
        if coord == end:
            break 
        for dx, dy in [(0, 1), (0,-1), (1,0), (-1,0)]:
            neighbor = (x+dx, y+dy)
            if not (0 <= neighbor[0] < NUM_ROWS and 0 <= neighbor[1] < NUM_COLS) or is_collision(neighbor, obstacles):
                continue
            if neighbor not in g_costs or g_costs[coord]+1 < g_costs[neighbor]:
                new_f_cost = g_costs[coord]+1+manhattan_distance(neighbor, end) # set f_cost of this neighbor cell to be the g_cost of the previous cell (coord) plus edge weight (which is 1 in this case) plus heuristic which is manhattan distance from this neighbor cell to the end cell
                f_costs[neighbor] = new_f_cost
                g_costs[neighbor] = g_costs[coord]+1
                parents[neighbor] = coord
                heapq.heappush(pq, (new_f_cost, neighbor))
    # need to retrace the path (if it exists) and return it
    # if path doesn't exist, return None
    path = []
    current = end
    while current != start:
        path.append(current)
        if current not in parents:
            # this means that there is no path from start to end
            return None
        current = parents[current]
    path.append(start)
    path.reverse()
    return path


def main():
    robot = Robot(0, 0)
    obstacles = generate_obstacles(300)
    goal = (random.randint(NUM_ROWS-10, NUM_ROWS-1), random.randint(NUM_COLS-10, NUM_COLS-1))
    path = aStar((robot.x, robot.y), goal, obstacles)
    step = 0
    running = True
    if path is None:
        print("No path exists")
        return
    # Simulation
    screen.fill(WHITE)
    draw_grid()
    for obstacle in obstacles:
        obstacle.draw()
    pygame.draw.rect(screen, RED, pygame.Rect(goal[0]*CELL_SIZE, goal[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                break
        if not running:
            break
        if step < len(path):
            dx, dy = path[step][0]-robot.x, path[step][1]-robot.y
            robot.move(dx, dy)
            robot.draw()
            step += 1
        robot.draw()
        pygame.display.flip()
        clock.tick(10) # 10 FPS
    print(f"Number of steps: {step}")

if __name__ == "__main__":
    main()
