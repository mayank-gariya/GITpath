import time 
from collections import deque
from typing import Generator
from graph.builder import GraphBuilder, SearchDirection
from algorithms.schemas import SearchResult, SearchGraph, Edge, ProgressUpdate
from graph.node import GraphNode

class BidirectionalBFS:
    
    def get_shortest_path_stream(
        self, start: str, target: str, builder: GraphBuilder
    ) -> Generator[ProgressUpdate, None, None]:
        start_time = time.time()
        
        start_clean = start.lower().strip()
        target_clean = target.lower().strip()
        
        # Track unique nodes seen to build the UI graph visualization
        nodes_map = {start_clean: GraphNode(username=start, avatar_url="", html_url="")}
        edges = []
        
        if start_clean == target_clean:
            res = SearchResult(
                found=True, path=[start], visited_count=1, search_depth=0,
                api_calls=0, elapsed_time=round(time.time() - start_time, 4),
                graph=SearchGraph(nodes=list(nodes_map.values()), edges=edges)
            )
            yield ProgressUpdate(type="final", visited_count=1, current_node=start, graph=res.graph, result=res)
            return
        
        # Forward search (exploring users the current user FOLLOWS)
        forward_queue = deque([start_clean])
        forward_visited = {start_clean}
        forward_parent = {start_clean: None}
        
        # Backward search (exploring FOLLOWERS who point to the current user)
        backward_queue = deque([target_clean])
        backward_visited = {target_clean}
        backward_parent = {target_clean: None}
        
        intersect_node = None
        
        while forward_queue and backward_queue:
            # Expand the smaller queue to optimize processing balance
            if len(forward_queue) <= len(backward_queue):
                current = forward_queue.popleft()
                direction = SearchDirection.FOLLOWING
                visited, parent, other_visited = forward_visited, forward_parent, backward_visited
            else:
                current = backward_queue.popleft()
                direction = SearchDirection.FOLLOWERS
                visited, parent, other_visited = backward_visited, backward_parent, forward_visited

            # Yield progress to Streamlit for every node popped
            current_graph = SearchGraph(nodes=list(nodes_map.values()), edges=list(edges))
            yield ProgressUpdate(type="progress", visited_count=len(forward_visited) + len(backward_visited), current_node=current, graph=current_graph)
                
            try:
                neighbors = builder.get_neighbors(current, direction=direction)
            except Exception:
                continue
                
            for neighbor in neighbors:
                neighbor_name = neighbor if isinstance(neighbor, str) else neighbor.username
                neighbor_clean = neighbor_name.lower().strip()
                
                if neighbor_clean not in visited:
                    visited.add(neighbor_clean)
                    parent[neighbor_clean] = current
                    queue_to_append = forward_queue if direction == SearchDirection.FOLLOWING else backward_queue
                    queue_to_append.append(neighbor_clean)
                    
                    # Track nodes & edges for graph rendering
                    if not isinstance(neighbor, str):
                        nodes_map[neighbor_clean] = neighbor
                    elif neighbor_clean not in nodes_map:
                        nodes_map[neighbor_clean] = GraphNode(username=neighbor_name, avatar_url="", html_url="")
                    
                    if direction == SearchDirection.FOLLOWING:
                        edges.append(Edge(source=current, target=neighbor_clean))
                    else:
                        edges.append(Edge(source=neighbor_clean, target=current))
                    
                    if neighbor_clean in other_visited:
                        intersect_node = neighbor_clean
                        break
            
            if intersect_node:
                break
                
        elapsed_time = time.time() - start_time
        
        if intersect_node:
            path = self._reconstruct_bidirectional_path(
                forward_parent, backward_parent, start_clean, target_clean, intersect_node
            )
            search_depth = len(path) - 1
            found = True
        else:
            path = []
            search_depth = 0
            found = False
            
        final_graph = SearchGraph(nodes=list(nodes_map.values()), edges=edges)
        res = SearchResult(
            found=found, path=path, visited_count=len(forward_visited) + len(backward_visited),
            search_depth=search_depth, api_calls=getattr(builder, "api_calls", 0),
            elapsed_time=round(elapsed_time, 4), graph=final_graph
        )
        yield ProgressUpdate(type="final", visited_count=len(forward_visited) + len(backward_visited), current_node=target, graph=final_graph, result=res)
        
    def _reconstruct_bidirectional_path(
        self, forward_parent: dict, backward_parent: dict, 
        start: str, target: str, intersect_node: str
    ) -> list[str]:
        forward_path = []
        current = intersect_node
        while current is not None:
            forward_path.append(current)
            current = forward_parent.get(current)
        forward_path.reverse()
        
        backward_path = []
        current = backward_parent.get(intersect_node)
        while current is not None:
            backward_path.append(current)
            current = backward_parent.get(current)
            
        return forward_path + backward_path