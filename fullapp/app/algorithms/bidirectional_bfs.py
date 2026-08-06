import time 
from collections import deque
from typing import Generator
from Backend.app.graph.builder import GraphBuilder, SearchDirection
from Backend.app.algorithms.schemas import SearchResult, SearchGraph, Edge, ProgressUpdate
from Backend.app.graph.node import GraphNode

class BidirectionalBFS:
    
    def get_shortest_path_stream(
        self, start: str, target: str, builder: GraphBuilder
    ) -> Generator[ProgressUpdate, None, None]:
        start_time = time.time()
        
        # 1. Normalize inputs to prevent case sensitivity traps
        start_clean = start.lower().strip()
        target_clean = target.lower().strip()
        
        # Initialize nodes mapping with lowercase keys
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

        # Dual-frontier queues for Bidirectional BFS
        forward_queue = deque([start_clean])
        forward_visited = {start_clean}
        forward_parent = {start_clean: None}
        
        backward_queue = deque([target_clean])
        backward_visited = {target_clean}
        backward_parent = {target_clean: None}
        
        # Ensure target node exists in map
        if target_clean not in nodes_map:
            nodes_map[target_clean] = GraphNode(username=target, avatar_url="", html_url="")

        intersect_node = None
        found = False
        MAX_VISITED = 5000  # Guardrail search limit
        node_counter = 0

        while forward_queue and backward_queue:
            if (len(forward_visited) + len(backward_visited)) >= MAX_VISITED:
                break

            # Balance optimization: Expand the smaller queue frontier
            if len(forward_queue) <= len(backward_queue):
                current = forward_queue.popleft()
                direction = SearchDirection.FOLLOWING
                current_visited = forward_visited
                current_parent = forward_parent
                other_visited = backward_visited
            else:
                current = backward_queue.popleft()
                direction = SearchDirection.FOLLOWERS
                current_visited = backward_visited
                current_parent = backward_parent
                other_visited = forward_visited

            # UI Performance optimization: stream updates every 10 nodes instead of every node
            node_counter += 1
            if node_counter % 10 == 0:
                current_graph = SearchGraph(nodes=list(nodes_map.values()), edges=list(edges))
                yield ProgressUpdate(
                    type="progress", 
                    visited_count=len(forward_visited) + len(backward_visited), 
                    current_node=current, 
                    graph=current_graph
                )
            
            try:
                neighbors = builder.get_neighbors(current, direction=direction)
            except Exception:
                continue
                
            for neighbor in neighbors:
                neighbor_name = neighbor if isinstance(neighbor, str) else neighbor.username
                neighbor_clean = neighbor_name.lower().strip()
                
                if neighbor_clean not in current_visited:
                    current_visited.add(neighbor_clean)
                    current_parent[neighbor_clean] = current
                    
                    # Track structural node mapping details safely
                    if not isinstance(neighbor, str):
                        nodes_map[neighbor_clean] = neighbor
                    elif neighbor_clean not in nodes_map:
                        nodes_map[neighbor_clean] = GraphNode(username=neighbor_name, avatar_url="", html_url="")
                    
                    # Append directed tracking structures
                    if direction == SearchDirection.FOLLOWING:
                        edges.append(Edge(source=current, target=neighbor_clean))
                    else:
                        edges.append(Edge(source=neighbor_clean, target=current))
                        
                    # 🎯 FIXED: Instant early-exit discovery inside the neighbor loop
                    if neighbor_clean in other_visited:
                        intersect_node = neighbor_clean
                        found = True
                        break
                        
                    current_queue = forward_queue if direction == SearchDirection.FOLLOWING else backward_queue
                    current_queue.append(neighbor_clean)
                    
            if found:
                break
                
        elapsed_time = time.time() - start_time
        path = []
        
        if found and intersect_node:
            # Reconstruct and stitch together the bidirectional branches
            path = self._reconstruct_bidirectional_path(
                forward_parent, backward_parent, start_clean, target_clean, intersect_node
            )
            
        final_graph = SearchGraph(nodes=list(nodes_map.values()), edges=edges)
        res = SearchResult(
            found=found, 
            path=path, 
            visited_count=len(forward_visited) + len(backward_visited),
            search_depth=max(0, len(path) - 1) if found else 0,
            api_calls=getattr(builder, "api_calls", 0),
            elapsed_time=round(elapsed_time, 4),
            graph=final_graph
        )
        yield ProgressUpdate(
            type="final", 
            visited_count=res.visited_count, 
            current_node=target, 
            graph=final_graph, 
            result=res
        )

    def _reconstruct_bidirectional_path(
        self, forward_parent: dict, backward_parent: dict, 
        start: str, target: str, intersect_node: str
    ) -> list[str]:
        """Stitches the forward path and inverted backward path together cleanly."""
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