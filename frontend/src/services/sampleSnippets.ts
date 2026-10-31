export interface CodeSample {
  id: string;
  name: string;
  language: string;
  source: string;
  label: 'Human-Written' | 'AI-Generated' | 'Synthetic UI Test';
  description: string;
  code: string;
}

export const SAMPLE_CODES: Record<string, CodeSample> = {
  human_lru: {
    id: 'human_lru',
    name: 'LRU Cache Lookup (CPython)',
    language: 'python',
    source: 'CPython collections.OrderedDict implementation (PSF-2.0)',
    label: 'Human-Written',
    description: 'Human-engineered doubly-linked list cache traversal with low-level index aliases and specific pointer mutations.',
    code: `def lru_cache_lookup(key, mapping, root, PREV=0, NEXT=1, KEY=2, RESULT=3):
    # Link structure: [PREV, NEXT, KEY, RESULT]
    link = mapping.get(key)
    if link is not None:
        link_prev, link_next, _key, result = link
        link_prev[NEXT] = link_next
        link_next[PREV] = link_prev
        last = root[PREV]
        last[NEXT] = root[PREV] = link
        link[PREV] = last
        link[NEXT] = root
        return result
    return None`
  },
  ai_lru: {
    id: 'ai_lru',
    name: 'LRU Cache Implementation (GPT-4)',
    language: 'python',
    source: 'Prompted GPT-4 Zero-Shot Generation',
    label: 'AI-Generated',
    description: 'Textbook object-oriented double linked list cache with standard docstrings, modular node creation, and textbook comments.',
    code: `class Node:
    """Represents a doubly linked list node for the cache."""
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """Least Recently Used (LRU) Cache with O(1) operations."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]

    def _remove(self, node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: Node) -> None:
        prev_tail = self.tail.prev
        prev_tail.next = node
        node.prev = prev_tail
        node.next = self.tail
        self.tail.prev = node`
  },
  human_dijkstra: {
    id: 'human_dijkstra',
    name: 'Dijkstra Shortest Path (Python-Algorithms)',
    language: 'python',
    source: 'Open Source Algorithms Repository (MIT)',
    label: 'Human-Written',
    description: 'Compact graph shortest path traversal utilizing heapq with dynamic dictionary comprehension and minimal comments.',
    code: `def dijkstra(graph, src):
    import heapq
    dist = {v: float('inf') for v in graph}
    dist[src] = 0
    pq = [(0, src)]
    visited = set()
    
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        
        for v, weight in graph[u].items():
            if d + weight < dist[v]:
                dist[v] = d + weight
                heapq.heappush(pq, (dist[v], v))
    return dist`
  },
  ai_dijkstra: {
    id: 'ai_dijkstra',
    name: 'Dijkstra with Path Reconstruction (GPT-4)',
    language: 'python',
    source: 'Prompted GPT-4 Zero-Shot Generation',
    label: 'AI-Generated',
    description: 'Verbose procedural implementation including full typing annotations, predecessors tracking, and formatted return dictionaries.',
    code: `import heapq
from typing import Dict, List, Tuple, Optional

def calculate_shortest_paths(
    adjacency_list: Dict[str, List[Tuple[str, float]]],
    source_node: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Computes shortest distances and tracks predecessor paths from source_node.
    """
    distances: Dict[str, float] = {node: float('inf') for node in adjacency_list}
    predecessors: Dict[str, Optional[str]] = {node: None for node in adjacency_list}
    distances[source_node] = 0.0

    priority_queue: List[Tuple[float, str]] = [(0.0, source_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, edge_weight in adjacency_list.get(current_node, []):
            calculated_distance = current_distance + edge_weight

            if calculated_distance < distances[neighbor]:
                distances[neighbor] = calculated_distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (calculated_distance, neighbor))

    return distances, predecessors`
  },
  human_bisect: {
    id: 'human_bisect',
    name: 'Binary Search Left (CPython Bisect)',
    language: 'python',
    source: 'CPython Lib/bisect.py (PSF-2.0)',
    label: 'Human-Written',
    description: 'Standard library binary search logic with strict integer midpoint calculation and direct while loop boundary narrowing.',
    code: `def bisect_left(a, x, lo=0, hi=None, *, key=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    if key is None:
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid
    else:
        while lo < hi:
            mid = (lo + hi) // 2
            if key(a[mid]) < x:
                lo = mid + 1
            else:
                hi = mid
    return lo`
  },
  ai_binary_search: {
    id: 'ai_binary_search',
    name: 'Standard Binary Search (Claude 3.5 Sonnet)',
    language: 'python',
    source: 'Prompted Claude 3.5 Sonnet Generation',
    label: 'AI-Generated',
    description: 'Explanatory binary search with guard clauses, step-by-step descriptive comments, and overflow prevention formula.',
    code: `def binary_search(elements: list, target_value) -> int:
    """
    Performs a binary search on a sorted list to locate target_value.
    Returns index if found, else -1.
    """
    if not elements:
        return -1

    left_index = 0
    right_index = len(elements) - 1

    while left_index <= right_index:
        # Calculate midpoint avoiding overflow
        mid_index = left_index + (right_index - left_index) // 2
        current_value = elements[mid_index]

        if current_value == target_value:
            return mid_index
        elif current_value < target_value:
            left_index = mid_index + 1
        else:
            right_index = mid_index - 1

    return -1`
  },
  human_js_debounce: {
    id: 'human_js_debounce',
    name: 'Debounce Utility (Lodash)',
    language: 'javascript',
    source: 'Lodash Open Source Library (MIT)',
    label: 'Human-Written',
    description: 'Production JavaScript closure debouncer with trailing invoke, timer clearance, and invocation context binding.',
    code: `function debounce(func, wait, options) {
  let lastArgs, lastThis, maxWait, result, timerId, lastCallTime;
  let lastInvokeTime = 0;
  let leading = false;
  let maxing = false;
  let trailing = true;

  function invokeFunc(time) {
    const args = lastArgs;
    const thisArg = lastThis;
    lastArgs = lastThis = undefined;
    lastInvokeTime = time;
    result = func.apply(thisArg, args);
    return result;
  }

  function startTimer(pendingFunc, waitTime) {
    return setTimeout(pendingFunc, waitTime);
  }

  return function debounced(...args) {
    const time = Date.now();
    const isInvoking = shouldInvoke(time);
    lastArgs = args;
    lastThis = this;
    lastCallTime = time;
    if (isInvoking) {
      if (timerId === undefined) {
        return leadingEdge(lastCallTime);
      }
    }
    return result;
  };
}`
  },
  ai_js_debounce: {
    id: 'ai_js_debounce',
    name: 'Debounce Function (GPT-4)',
    language: 'javascript',
    source: 'Prompted GPT-4 Generation',
    label: 'AI-Generated',
    description: 'Textbook TypeScript-ready JavaScript debounce wrapper with parameter rest patterns and generic timeout handling.',
    code: `/**
 * Creates a debounced function that delays invoking func until after wait milliseconds.
 * @param {Function} func The target function to debounce.
 * @param {number} delay The number of milliseconds to delay.
 * @returns {Function} Returns the new debounced function.
 */
function createDebouncedHandler(func, delay = 300) {
  let timeoutId = null;

  return function (...args) {
    const context = this;

    // Clear existing timer if triggered again within delay window
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      func.apply(context, args);
      timeoutId = null;
    }, delay);
  };
}`
  }
};
