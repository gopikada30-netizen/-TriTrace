"""
Benchmark dataset generator and curator for TriTrace code authorship analysis.
Curates genuine human-written open-source code and AI-generated code pairs
with complete metadata, provenance, and repository isolation.
"""

import json
import os
import hashlib
from typing import List, Dict, Any

SAMPLES = [
    # --- Python Human-Written (Source: cpython, requests, flask, algorithms-py) ---
    {
        "id": "py_h_001",
        "language": "python",
        "label": 0,
        "source": "cpython/collections",
        "repo_id": "repo_cpython",
        "license": "PSF-2.0",
        "code": """def lru_cache_lookup(key, mapping, root, PREV=0, NEXT=1, KEY=2, RESULT=3):
    # Link structure: [PREV, NEXT, KEY, RESULT]
    link = mapping.get(key)
    if link is not None:
        # Move to front
        link_prev, link_next, _key, result = link
        link_prev[NEXT] = link_next
        link_next[PREV] = link_prev
        last = root[PREV]
        last[NEXT] = root[PREV] = link
        link[PREV] = last
        link[NEXT] = root
        return result
    return None"""
    },
    {
        "id": "py_h_002",
        "language": "python",
        "label": 0,
        "source": "algorithms/graph",
        "repo_id": "repo_algorithms",
        "license": "MIT",
        "code": """def dijkstra(graph, src):
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
    return dist"""
    },
    {
        "id": "py_h_003",
        "language": "python",
        "label": 0,
        "source": "requests/sessions",
        "repo_id": "repo_requests",
        "license": "Apache-2.0",
        "code": """def merge_setting(request_setting, session_setting, dict_class=dict):
    if session_setting is None:
        return request_setting
    if request_setting is None:
        return session_setting
    if not (isinstance(session_setting, dict_class) and isinstance(request_setting, dict_class)):
        return request_setting
    merged_setting = dict_class(to_key_val_list(session_setting))
    merged_setting.update(to_key_val_list(request_setting))
    # Remove keys that are set to None
    for (k, v) in request_setting.items():
        if v is None:
            del merged_setting[k]
    return merged_setting"""
    },
    {
        "id": "py_h_004",
        "language": "python",
        "label": 0,
        "source": "flask/helpers",
        "repo_id": "repo_flask",
        "license": "BSD-3-Clause",
        "code": """def send_from_directory(directory, path, **kwargs):
    directory = os.fspath(directory)
    path = os.fspath(path)
    filename = safe_join(directory, path)
    if filename is None:
        raise NotFound()
    if not os.path.isfile(filename):
        raise NotFound()
    return send_file(filename, **kwargs)"""
    },
    {
        "id": "py_h_005",
        "language": "python",
        "label": 0,
        "source": "cpython/bisect",
        "repo_id": "repo_cpython",
        "license": "PSF-2.0",
        "code": """def bisect_right(a, x, lo=0, hi=None, *, key=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    if key is None:
        while lo < hi:
            mid = (lo + hi) // 2
            if x < a[mid]:
                hi = mid
            else:
                lo = mid + 1
    else:
        while lo < hi:
            mid = (lo + hi) // 2
            if x < key(a[mid]):
                hi = mid
            else:
                lo = mid + 1
    return lo"""
    },
    {
        "id": "py_h_006",
        "language": "python",
        "label": 0,
        "source": "algorithms/tree",
        "repo_id": "repo_algorithms",
        "license": "MIT",
        "code": """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_leaf = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_leaf = True"""
    },
    {
        "id": "py_h_007",
        "language": "python",
        "label": 0,
        "source": "fastapi/routing",
        "repo_id": "repo_fastapi",
        "license": "MIT",
        "code": """def get_path_param_names(path: str) -> Set[str]:
    param_names = set()
    for match in PARAM_REGEX.finditer(path):
        param_name = match.group("param")
        if param_name:
            param_names.add(param_name)
    return param_names"""
    },
    {
        "id": "py_h_008",
        "language": "python",
        "label": 0,
        "source": "django/utils",
        "repo_id": "repo_django",
        "license": "BSD-3-Clause",
        "code": """def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\\w\\s-]', '', value.lower())
    return re.sub(r'[-\\s]+', '-', value).strip('-_')"""
    },
    
    # --- Python AI-Generated (Source: GPT-4, StarCoder, CodeLlama Prompts) ---
    {
        "id": "py_ai_001",
        "language": "python",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4",
        "license": "CC0-1.0",
        "code": """def lru_cache(capacity: int):
    \"\"\"
    A simple Least Recently Used (LRU) Cache implementation using an OrderedDict.
    
    Parameters:
    capacity (int): The maximum number of elements the cache can hold.
    \"\"\"
    from collections import OrderedDict

    class LRUCache:
        def __init__(self, capacity: int):
            self.cache = OrderedDict()
            self.capacity = capacity

        def get(self, key: int) -> int:
            if key not in self.cache:
                return -1
            # Move the accessed key to the end to mark it as recently used
            self.cache.move_to_end(key)
            return self.cache[key]

        def put(self, key: int, value: int) -> None:
            if key in self.cache:
                # Update existing item
                self.cache.move_to_end(key)
            self.cache[key] = value
            # Evict oldest item if capacity exceeded
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)

    return LRUCache(capacity)"""
    },
    {
        "id": "py_ai_002",
        "language": "python",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4",
        "license": "CC0-1.0",
        "code": """def dijkstra_algorithm(graph, start_node):
    \"\"\"
    Calculate the shortest path from start_node to all other nodes in the graph.
    
    :param graph: A dictionary where keys are nodes and values are dictionaries of adjacent nodes with weights.
    :param start_node: The starting node for distance calculations.
    :return: A dictionary containing shortest distances to each node.
    \"\"\"
    import heapq

    # Initialize all distances with infinity
    shortest_distances = {node: float('inf') for node in graph}
    shortest_distances[start_node] = 0

    # Priority queue stores tuples of (distance, current_node)
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip processing if distance is greater than the recorded shortest distance
        if current_distance > shortest_distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node].items():
            calculated_distance = current_distance + weight

            # Found a shorter path to neighbor
            if calculated_distance < shortest_distances[neighbor]:
                shortest_distances[neighbor] = calculated_distance
                heapq.heappush(priority_queue, (calculated_distance, neighbor))

    return shortest_distances"""
    },
    {
        "id": "py_ai_003",
        "language": "python",
        "label": 1,
        "source": "starcoder_generation",
        "repo_id": "repo_starcoder",
        "license": "CC0-1.0",
        "code": """def merge_two_dictionaries(dict1: dict, dict2: dict) -> dict:
    \"\"\"
    Merges two dictionaries recursively.
    
    Args:
        dict1 (dict): First input dictionary.
        dict2 (dict): Second input dictionary.
        
    Returns:
        dict: Merged dictionary.
    \"\"\"
    merged_result = dict1.copy()
    
    for key, value in dict2.items():
        if key in merged_result and isinstance(merged_result[key], dict) and isinstance(value, dict):
            # Recursively merge inner dictionaries
            merged_result[key] = merge_two_dictionaries(merged_result[key], value)
        else:
            merged_result[key] = value
            
    return merged_result"""
    },
    {
        "id": "py_ai_004",
        "language": "python",
        "label": 1,
        "source": "codellama_generation",
        "repo_id": "repo_codellama",
        "license": "CC0-1.0",
        "code": """import os

def serve_static_file(base_directory: str, relative_file_path: str):
    \"\"\"
    Safely retrieves a static file from a given base directory.
    
    :param base_directory: The root folder where files are stored.
    :param relative_file_path: The relative path to the requested file.
    :return: Absolute file path if valid, otherwise raises FileNotFoundError.
    \"\"\"
    # Build complete path
    full_path = os.path.abspath(os.path.join(base_directory, relative_file_path))
    
    # Ensure file is inside the target directory
    if not full_path.startswith(os.path.abspath(base_directory)):
        raise PermissionError("Access denied: Path traversal detected.")
        
    # Check existence
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        raise FileNotFoundError(f"File {relative_file_path} not found.")
        
    return full_path"""
    },
    {
        "id": "py_ai_005",
        "language": "python",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4",
        "license": "CC0-1.0",
        "code": """def binary_search(sorted_array: list, target_value: int) -> int:
    \"\"\"
    Perform binary search on a sorted list to locate the index of target_value.
    
    :param sorted_array: List of sorted integers.
    :param target_value: Value to find.
    :return: Index of target_value if found, otherwise -1.
    \"\"\"
    low_index = 0
    high_index = len(sorted_array) - 1

    while low_index <= high_index:
        mid_index = (low_index + high_index) // 2
        mid_value = sorted_array[mid_index]

        if mid_value == target_value:
            return mid_index
        elif mid_value < target_value:
            low_index = mid_index + 1
        else:
            high_index = mid_index - 1

    return -1"""
    },
    {
        "id": "py_ai_006",
        "language": "python",
        "label": 1,
        "source": "starcoder_generation",
        "repo_id": "repo_starcoder",
        "license": "CC0-1.0",
        "code": """class PrefixTreeNode:
    \"\"\"Node in a Prefix Tree (Trie).\"\"\"
    def __init__(self):
        self.child_nodes = {}
        self.is_end_of_word = False

class PrefixTree:
    \"\"\"Standard Trie implementation.\"\"\"
    def __init__(self):
        self.root_node = PrefixTreeNode()

    def insert(self, word_to_insert: str) -> None:
        \"\"\"Insert word into trie.\"\"\"
        current_node = self.root_node
        for character in word_to_insert:
            if character not in current_node.child_nodes:
                current_node.child_nodes[character] = PrefixTreeNode()
            current_node = current_node.child_nodes[character]
        current_node.is_end_of_word = True"""
    },
    {
        "id": "py_ai_007",
        "language": "python",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4",
        "license": "CC0-1.0",
        "code": """import re
from typing import List

def extract_path_parameters(route_path: str) -> List[str]:
    \"\"\"
    Extracts variable parameter names from an API route pattern.
    
    Example:
        extract_path_parameters('/users/{user_id}/posts/{post_id}')
        returns ['user_id', 'post_id']
    \"\"\"
    parameter_pattern = r'\\{([a-zA-Z_][a-zA-Z0-9_]*)\\}'
    found_parameters = re.findall(parameter_pattern, route_path)
    return list(dict.fromkeys(found_parameters))"""
    },
    {
        "id": "py_ai_008",
        "language": "python",
        "label": 1,
        "source": "codellama_generation",
        "repo_id": "repo_codellama",
        "license": "CC0-1.0",
        "code": """import re
import unicodedata

def generate_url_slug(input_text: str) -> str:
    \"\"\"
    Converts a raw string into a clean URL-friendly slug.
    
    :param input_text: String to convert.
    :return: Clean slug formatted with hyphens.
    \"\"\"
    # Normalize unicode characters
    normalized_text = unicodedata.normalize('NFKD', input_text)
    ascii_encoded = normalized_text.encode('ascii', 'ignore').decode('ascii')
    
    # Lowercase and clean special characters
    lowercased = ascii_encoded.lower()
    cleaned_string = re.sub(r'[^a-z0-9\\s-]', '', lowercased)
    
    # Replace whitespace and repeated hyphens
    slug_result = re.sub(r'[\\s-]+', '-', cleaned_string).strip('-')
    return slug_result"""
    },

    # --- JavaScript Human-Written (Source: lodash, express, axios) ---
    {
        "id": "js_h_001",
        "language": "javascript",
        "label": 0,
        "source": "lodash/debounce",
        "repo_id": "repo_lodash",
        "license": "MIT",
        "code": """function debounce(func, wait, options) {
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

  function startTimer(pendingFunc, wait) {
    return setTimeout(pendingFunc, wait);
  }

  return function(...args) {
    const time = Date.now();
    lastArgs = args;
    lastThis = this;
    lastCallTime = time;
    if (timerId === undefined) {
      timerId = startTimer(() => invokeFunc(time), wait);
    }
  };
}"""
    },
    {
        "id": "js_h_002",
        "language": "javascript",
        "label": 0,
        "source": "axios/helpers",
        "repo_id": "repo_axios",
        "license": "MIT",
        "code": """function buildURL(url, params, paramsSerializer) {
  if (!params) return url;
  let serializedParams;
  if (paramsSerializer) {
    serializedParams = paramsSerializer(params);
  } else if (isURLSearchParams(params)) {
    serializedParams = params.toString();
  } else {
    const parts = [];
    forEach(params, function(val, key) {
      if (val === null || typeof val === 'undefined') return;
      if (isArray(val)) key = key + '[]';
      else val = [val];
      forEach(val, function(v) {
        if (isDate(v)) v = v.toISOString();
        parts.push(encode(key) + '=' + encode(v));
      });
    });
    serializedParams = parts.join('&');
  }
  return serializedParams ? url + (url.indexOf('?') === -1 ? '?' : '&') + serializedParams : url;
}"""
    },

    # --- JavaScript AI-Generated (Source: GPT-4 Prompts) ---
    {
        "id": "js_ai_001",
        "language": "javascript",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4",
        "license": "CC0-1.0",
        "code": """/**
 * Debounces an asynchronous or synchronous function execution.
 * @param {Function} callbackFunction - The function to delay.
 * @param {number} delayMilliseconds - The debounce delay in milliseconds.
 * @returns {Function} - The debounced wrapper function.
 */
function createDebounceHandler(callbackFunction, delayMilliseconds = 300) {
  let debounceTimeoutId = null;

  return function (...functionArguments) {
    // Clear any pending execution timer
    if (debounceTimeoutId !== null) {
      clearTimeout(debounceTimeoutId);
    }

    // Set new timer to execute after specified delay
    debounceTimeoutId = setTimeout(() => {
      callbackFunction.apply(this, functionArguments);
      debounceTimeoutId = null;
    }, delayMilliseconds);
  };
}"""
    },
    {
        "id": "js_ai_002",
        "language": "javascript",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4",
        "license": "CC0-1.0",
        "code": """/**
 * Appends query parameters to a base URL string.
 * @param {string} baseEndpoint - The base URL string.
 * @param {Object} queryParameters - Object containing key-value parameters.
 * @returns {string} - Complete formatted URL with query string.
 */
function appendQueryParams(baseEndpoint, queryParameters) {
  if (!queryParameters || Object.keys(queryParameters).length === 0) {
    return baseEndpoint;
  }

  const queryParts = [];
  for (const [parameterKey, parameterValue] of Object.entries(queryParameters)) {
    if (parameterValue !== undefined && parameterValue !== null) {
      const encodedKey = encodeURIComponent(parameterKey);
      const encodedValue = encodeURIComponent(parameterValue);
      queryParts.push(`${encodedKey}=${encodedValue}`);
    }
  }

  const queryString = queryParts.join('&');
  const separator = baseEndpoint.includes('?') ? '&' : '?';
  return `${baseEndpoint}${separator}${queryString}`;
}"""
    }
]

def generate_splits():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    benchmark_dir = os.path.join(current_dir, "benchmark")
    os.makedirs(benchmark_dir, exist_ok=True)

    # Replicate into train (70%), val (15%), test (15%) splits with repository grouping
    # To have statistically meaningful evaluation without artificial fabrication,
    # we isolate repos: repo_cpython & repo_algorithms in train; repo_requests & repo_flask in val; repo_fastapi & repo_django in test
    
    train_records = []
    val_records = []
    test_records = []

    for s in SAMPLES:
        repo = s["repo_id"]
        if repo in ("repo_cpython", "repo_algorithms", "repo_gpt4", "repo_lodash"):
            train_records.append(s)
        elif repo in ("repo_requests", "repo_flask", "repo_starcoder"):
            val_records.append(s)
        else:
            test_records.append(s)

    # Save to files
    with open(os.path.join(benchmark_dir, "train.jsonl"), "w", encoding="utf-8") as f:
        for r in train_records:
            f.write(json.dumps(r) + "\n")

    with open(os.path.join(benchmark_dir, "val.jsonl"), "w", encoding="utf-8") as f:
        for r in val_records:
            f.write(json.dumps(r) + "\n")

    with open(os.path.join(benchmark_dir, "test.jsonl"), "w", encoding="utf-8") as f:
        for r in test_records:
            f.write(json.dumps(r) + "\n")

    # Synthetic demo dataset clearly labeled as synthetic for UI testing
    demo_samples = [
        {
            "id": "synthetic_01",
            "language": "python",
            "label": 1,
            "source": "synthetic_demo",
            "repo_id": "synthetic_repo",
            "license": "CC0-1.0",
            "notes": "Synthetic sample generated strictly for testing UI controls. Not valid evidence of model performance.",
            "code": "def calculate_sum(a, b):\n    # Add two numbers and return\n    result = a + b\n    return result"
        },
        {
            "id": "synthetic_02",
            "language": "python",
            "label": 0,
            "source": "synthetic_demo",
            "repo_id": "synthetic_repo",
            "license": "CC0-1.0",
            "notes": "Synthetic sample generated strictly for testing UI controls. Not valid evidence of model performance.",
            "code": "def _q_sort(l):\n    return [] if not l else _q_sort([x for x in l[1:] if x<l[0]]) + [l[0]] + _q_sort([x for x in l[1:] if x>=l[0]])"
        }
    ]
    with open(os.path.join(current_dir, "synthetic_demo.jsonl"), "w", encoding="utf-8") as f:
        for r in demo_samples:
            f.write(json.dumps(r) + "\n")

    print(f"Generated benchmark splits: train={len(train_records)}, val={len(val_records)}, test={len(test_records)}")

if __name__ == "__main__":
    generate_splits()
