import heapq
import time
from collections import deque

goal = [[1,2,3],[4,5,6],[7,8,0]]

def serialize(state):
    return str(state)

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i,j

def get_neighbors(state):
    x,y = find_zero(state)
    moves = []
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx,dy in directions:
        nx,ny = x+dx, y+dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            moves.append(new_state)
    return moves

# 🔹 BFS
def bfs(start):
    start_time = time.time()
    queue = deque([(start, [])])
    visited = set()
    nodes_expanded = 0   # 🔥 เพิ่ม

    while queue:
        state, path = queue.popleft()
        nodes_expanded += 1   # 🔥 เพิ่ม

        if serialize(state) in visited:
            continue
        visited.add(serialize(state))

        if state == goal:
            return {
                "steps": len(path),
                "time": time.time()-start_time,
                "nodes": nodes_expanded,   # 🔥 เพิ่ม
                "path": path
            }

        for nxt in get_neighbors(state):
            queue.append((nxt, path+[nxt]))
    return None

# 🔹 DFS
def dfs(start, limit=50):
    start_time = time.time()
    stack = [(start, [], 0)]
    visited = set()
    nodes_expanded = 0   # 🔥 เพิ่ม

    while stack:
        state, path, depth = stack.pop()
        nodes_expanded += 1   # 🔥 เพิ่ม

        if serialize(state) in visited or depth > limit:
            continue
        visited.add(serialize(state))

        if state == goal:
            return {
                "steps": len(path),
                "time": time.time()-start_time,
                "nodes": nodes_expanded,   # 🔥 เพิ่ม
                "path": path
            }

        for nxt in get_neighbors(state):
            stack.append((nxt, path+[nxt], depth+1))

    return None

# 🔹 A*
def heuristic(state):
    goal_pos = {1:(0,0),2:(0,1),3:(0,2),
                4:(1,0),5:(1,1),6:(1,2),
                7:(2,0),8:(2,1)}
    dist = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                x,y = goal_pos[val]
                dist += abs(x-i)+abs(y-j)
    return dist

def astar(start):
    start_time = time.time()
    pq = []
    heapq.heappush(pq, (0, start, []))
    visited = set()

    nodes_expanded = 0   # 🔥 เพิ่ม

    while pq:
        cost, state, path = heapq.heappop(pq)
        nodes_expanded += 1   # 🔥 เพิ่ม

        if serialize(state) in visited:
            continue
        visited.add(serialize(state))

        if state == goal:
            time_used = time.time() - start_time   # 🔥 เพิ่ม
            steps = len(path)   # 🔥 แก้ตรงนี้

            return {
                "steps": steps,
                "time": time_used,
                "nodes": nodes_expanded,
                "path": path
            }

        for nxt in get_neighbors(state):
            new_cost = len(path) + heuristic(nxt)
            heapq.heappush(pq, (new_cost, nxt, path + [nxt]))

    return None