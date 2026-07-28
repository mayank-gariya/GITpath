import time
from collections import deque
from typing import Generator
from graph.builder import GraphBuilder
from algorithms.schemas import SearchResult, SearchGraph, Edge, ProgressUpdate
from graph.node import GraphNode

class BFS:
    
    def get_shortest_path_stream(
        self, start: str, target: str, builder: GraphBuilder
    ) -> Generator[ProgressUpdate, None, None]:
        start_time = time.time()
        
        # Track unique nodes seen to avoid duplicate GraphNode objects in our graph payload
        nodes_map = {start: GraphNode(username=start, avatar_url="", html_url="")}
        edges = []
        
        if start == target:
            res = SearchResult(
                found=True, path=[start], visited_count=1, search_depth=0,
                api_calls=0, elapsed_time=round(time.time() - start_time, 4),
                graph=SearchGraph(nodes=list(nodes_map.values()), edges=edges)
            )
            yield ProgressUpdate(type="final", visited_count=1, current_node=start, graph=res.graph, result=res)
            return

        queue = deque([start])
        visited = {start}
        parent = {}
        found = False
        
        while queue:
            current = queue.popleft()
            
            # Yield progress to the client for every node we pop and start processing
            current_graph = SearchGraph(nodes=list(nodes_map.values()), edges=list(edges))
            yield ProgressUpdate(type="progress", visited_count=len(visited), current_node=current, graph=current_graph)
            
            if current == target:
                found = True
                break
            
            neighbors = builder.get_neighbors(current)
            
            for neighbor in neighbors:
                is_str = isinstance(neighbor, str)
                neighbor_name = neighbor if is_str else neighbor.username
                
                if neighbor_name not in visited:
                    visited.add(neighbor_name)
                    parent[neighbor_name] = current
                    
                    # Track nodes & edges for Feature 3
                    if not is_str:
                        nodes_map[neighbor_name] = neighbor
                    elif neighbor_name not in nodes_map:
                        nodes_map[neighbor_name] = GraphNode(username=neighbor_name, avatar_url="", html_url="")
                    
                    edges.append(Edge(source=current, target=neighbor_name))
                    queue.append(neighbor_name)
                    
        elapsed_time = time.time() - start_time
        path = self._reconstruct_path(parent, start, target) if found else []
        
        final_graph = SearchGraph(nodes=list(nodes_map.values()), edges=edges)
        res = SearchResult(
            found=found, path=path, visited_count=len(visited),
            search_depth=len(path) - 1 if found else 0,
            api_calls=getattr(builder, "api_calls", 0),
            elapsed_time=round(elapsed_time, 4),
            graph=final_graph
        )
        yield ProgressUpdate(type="final", visited_count=len(visited), current_node=target, graph=final_graph, result=res)

    def _reconstruct_path(self, parent: dict[str, str], start: str, target: str) -> list[str]:
        path = []
        current = target
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()
        return path