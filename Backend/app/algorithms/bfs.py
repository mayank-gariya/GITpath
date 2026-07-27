from collections import deque
from app.graph.builder import GraphBuilder
from app.algorithms.schemas import SearchResult
import time 

class BFS:
    
    def get_shortest_path(self,start:str,target:str,builder:GraphBuilder)->SearchResult:
        # time 
        start_time = time.time()
        # if targest is found then stop and return node 
        if start == target:
            return SearchResult(
                found=True,
                path=[start],
                visited_count=1,
                search_depth=0,
                api_calls=0,
                elapsed_time= time.time() - start_time
            )
        
        queue = deque([start])
        visited = {start}
        parent = {}
        depth = {start:0}
        found = False
        
        while queue:
            current = queue.popleft()
            
            if current == target:
                found = True
                break
            
            # fetch neighbours from the graph builder
            neighbors = builder.get_neighbors(current)
            
            for neighbor in neighbors:
                # If get_neighbors returns raw strings,
                neighbors_name = neighbor if isinstance(neighbor,str) else neighbor.username
                
                if neighbors_name not in visited:
                    visited.add(neighbors_name)
                    parent[neighbors_name] = current
                    depth[neighbors_name] = depth[current] + 1
                    queue.append(neighbors_name)
                    
        elapsed_time = time.time() - start_time
        
        # reconstruct 
        if found:
            path = self._reconstruct_path(parent,start,target)
            search_depth = len(path) -1
        else:
            path = []
            search_depth = 0

        return SearchResult(
            found=found,
            path=path,
            visited_count=len(visited),
            search_depth=search_depth,
            api_calls=getattr(builder, "api_calls", 0), 
            elapsed_time=round(elapsed_time, 4)
        )

    def _reconstruct_path(
        self, parent: dict[str, str], start: str, target: str
    ) -> list[str]:
        path = []
        current = target
        
        while current is not None   :
            path.append(current)
            
            if current is None:
                return []
            
            current = parent[current]
            
        path.append(start)
        path.reverse()  
        return path
        