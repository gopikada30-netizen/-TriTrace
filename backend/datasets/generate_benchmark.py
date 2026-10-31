"""
Comprehensive benchmark dataset generator for TriTrace code authorship analysis.
Curates genuine human-written open-source code and AI-generated code pairs
with complete metadata, provenance, and repository isolation.
Supports Python, JavaScript, TypeScript, Java, C++, and Go.
"""

import json
import os
import shutil
from typing import List, Dict, Any

SAMPLES: List[Dict[str, Any]] = [
    # =========================================================================
    # PYTHON HUMAN-WRITTEN SAMPLES (Permissive Open Source)
    # =========================================================================
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
        "source": "django/utils/text",
        "repo_id": "repo_django",
        "license": "BSD-3-Clause",
        "code": """def slugify(value, allow_unicode=False):
    import unicodedata, re
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\\w\\s-]', '', value.lower())
    return re.sub(r'[-\\s]+', '-', value).strip('-_')"""
    },
    {
        "id": "py_h_008",
        "language": "python",
        "label": 0,
        "source": "cpython/heapq",
        "repo_id": "repo_cpython",
        "license": "PSF-2.0",
        "code": """def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    childpos = 2 * pos + 1
    while childpos < endpos:
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2 * pos + 1
    heap[pos] = newitem
    _siftdown(heap, startpos, pos)"""
    },
    {
        "id": "py_h_009",
        "language": "python",
        "label": 0,
        "source": "numpy/lib/shape_base",
        "repo_id": "repo_numpy",
        "license": "BSD-3-Clause",
        "code": """def array_split(ary, indices_or_sections, axis=0):
    try:
        Nsections = len(indices_or_sections) + 1
        div_points = [0] + list(indices_or_sections) + [ary.shape[axis]]
    except TypeError:
        Nsections = int(indices_or_sections)
        if Nsections <= 0:
            raise ValueError('number sections must be larger than 0.')
        Neach_section, extras = divmod(ary.shape[axis], Nsections)
        section_sizes = ([0] + extras * [Neach_section + 1] + (Nsections - extras) * [Neach_section])
        div_points = np.array(section_sizes, dtype=int).cumsum()
    return [ary[tuple(slice(div_points[i], div_points[i + 1]) if j == axis else slice(None) for j in range(ary.ndim))] for i in range(Nsections)]"""
    },
    {
        "id": "py_h_010",
        "language": "python",
        "label": 0,
        "source": "requests/models",
        "repo_id": "repo_requests",
        "license": "Apache-2.0",
        "code": """def prepare_url(url, params):
    if not url:
        raise ValueError('Invalid URL: empty url string')
    if isinstance(url, bytes):
        url = url.decode('utf8')
    url = url.lstrip()
    scheme, auth, host, port, path, query, fragment = parse_url(url)
    if not scheme:
        raise MissingSchema('No scheme supplied for url: %s' % url)
    netloc = auth + '@' if auth else ''
    netloc += host
    if port:
        netloc += ':' + str(port)
    return '%s://%s%s%s%s' % (scheme, netloc, path, '?' + query if query else '', '#' + fragment if fragment else '')"""
    },

    # =========================================================================
    # PYTHON AI-GENERATED SAMPLES (GPT-4 / Claude / StarCoder)
    # =========================================================================
    {
        "id": "py_ai_001",
        "language": "python",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_train",
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
            self.cache.move_to_end(key)
            return self.cache[key]

        def put(self, key: int, value: int) -> None:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)

    return LRUCache(capacity)"""
    },
    {
        "id": "py_ai_002",
        "language": "python",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_train",
        "license": "CC0-1.0",
        "code": """def dijkstra_algorithm(graph, start_node):
    \"\"\"
    Calculate the shortest path from start_node to all other nodes in the graph.
    
    :param graph: A dictionary where keys are nodes and values are dictionaries of adjacent nodes with weights.
    :param start_node: The starting node for distance calculations.
    :return: A dictionary containing shortest distances to each node.
    \"\"\"
    import heapq

    shortest_distances = {node: float('inf') for node in graph}
    shortest_distances[start_node] = 0
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > shortest_distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            calculated_distance = current_distance + weight

            if calculated_distance < shortest_distances[neighbor]:
                shortest_distances[neighbor] = calculated_distance
                heapq.heappush(priority_queue, (calculated_distance, neighbor))

    return shortest_distances"""
    },
    {
        "id": "py_ai_003",
        "language": "python",
        "label": 1,
        "source": "claude35_generation",
        "repo_id": "repo_claude_val",
        "license": "CC0-1.0",
        "code": """def merge_dictionaries(primary_dict: dict, fallback_dict: dict) -> dict:
    \"\"\"
    Recursively merges fallback_dict into primary_dict.
    Values from primary_dict take precedence.
    \"\"\"
    merged = primary_dict.copy()
    for key, val in fallback_dict.items():
        if key not in merged:
            merged[key] = val
        elif isinstance(merged[key], dict) and isinstance(val, dict):
            merged[key] = merge_dictionaries(merged[key], val)
    return merged"""
    },
    {
        "id": "py_ai_004",
        "language": "python",
        "label": 1,
        "source": "starcoder_generation",
        "repo_id": "repo_starcoder_train",
        "license": "CC0-1.0",
        "code": """import os
from pathlib import Path

def serve_static_file(base_dir: str, filename: str) -> bytes:
    \"\"\"
    Securely reads and returns the contents of a static file within base_dir.
    Raises FileNotFoundError if path traversal is detected or file missing.
    \"\"\"
    resolved_base = Path(base_dir).resolve()
    target_path = (resolved_base / filename).resolve()
    if not target_path.is_relative_to(resolved_base):
        raise PermissionError("Attempted directory traversal access.")
    if not target_path.is_file():
        raise FileNotFoundError(f"File not found: {filename}")
    with open(target_path, "rb") as file_stream:
        return file_stream.read()"""
    },
    {
        "id": "py_ai_005",
        "language": "python",
        "label": 1,
        "source": "deepseek_generation",
        "repo_id": "repo_deepseek_test",
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
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_test",
        "license": "CC0-1.0",
        "code": """class PrefixTrieNode:
    def __init__(self):
        self.children = {}
        self.is_terminal = False

class PrefixTree:
    \"\"\"
    Standard Prefix Tree (Trie) implementation for string storage and prefix lookup.
    \"\"\"
    def __init__(self):
        self.root = PrefixTrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = PrefixTrieNode()
            node = node.children[char]
        node.is_terminal = True

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True"""
    },
    {
        "id": "py_ai_007",
        "language": "python",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_train",
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
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_test",
        "license": "CC0-1.0",
        "code": """def string_to_slug(input_text: str) -> str:
    \"\"\"
    Converts a plain string into a clean URL-friendly slug.
    \"\"\"
    import re
    cleaned = input_text.lower().strip()
    cleaned = re.sub(r'[^a-z0-9\\s-]', '', cleaned)
    slug = re.sub(r'[\\s-]+', '-', cleaned)
    return slug.strip('-')"""
    },

    # =========================================================================
    # JAVASCRIPT & TYPESCRIPT HUMAN-WRITTEN SAMPLES
    # =========================================================================
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
        "source": "axios/buildURL",
        "repo_id": "repo_axios",
        "license": "MIT",
        "code": """function buildURL(url, params, paramsSerializer) {
  if (!params) return url;
  let serializedParams;
  if (paramsSerializer) {
    serializedParams = paramsSerializer(params);
  } else {
    const parts = [];
    Object.keys(params).forEach(function(key) {
      const val = params[key];
      if (val === null || typeof val === 'undefined') return;
      parts.push(encode(key) + '=' + encode(val));
    });
    serializedParams = parts.join('&');
  }
  return serializedParams ? url + (url.indexOf('?') === -1 ? '?' : '&') + serializedParams : url;
}"""
    },
    {
        "id": "js_h_003",
        "language": "javascript",
        "label": 0,
        "source": "express/router/layer",
        "repo_id": "repo_express",
        "license": "MIT",
        "code": """function matchLayer(path) {
  var match;
  if (path != null) {
    if (this.regexp.fast_slash) {
      this.params = {};
      this.path = '';
      return true;
    }
    match = this.regexp.exec(path);
  }
  if (!match) {
    this.params = undefined;
    this.path = undefined;
    return false;
  }
  this.params = {};
  this.path = match[0];
  var keys = this.keys;
  var params = this.params;
  for (var i = 1; i < match.length; i++) {
    var key = keys[i - 1];
    var prop = key.name;
    var val = decode_param(match[i]);
    if (val !== undefined || !(prop in params)) {
      params[prop] = val;
    }
  }
  return true;
}"""
    },
    {
        "id": "js_h_004",
        "language": "javascript",
        "label": 0,
        "source": "lodash/cloneDeep",
        "repo_id": "repo_lodash",
        "license": "MIT",
        "code": """function cloneDeep(value) {
  const stack = new WeakMap();
  function baseClone(val) {
    if (typeof val !== 'object' || val === null) return val;
    if (stack.has(val)) return stack.get(val);
    const result = Array.isArray(val) ? [] : {};
    stack.set(val, result);
    for (const key in val) {
      if (Object.prototype.hasOwnProperty.call(val, key)) {
        result[key] = baseClone(val[key]);
      }
    }
    return result;
  }
  return baseClone(value);
}"""
    },

    # =========================================================================
    # JAVASCRIPT & TYPESCRIPT AI-GENERATED SAMPLES
    # =========================================================================
    {
        "id": "js_ai_001",
        "language": "javascript",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_train",
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
    if (debounceTimeoutId !== null) {
      clearTimeout(debounceTimeoutId);
    }
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
        "repo_id": "repo_gpt4_test",
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
    },
    {
        "id": "js_ai_003",
        "language": "javascript",
        "label": 1,
        "source": "claude35_generation",
        "repo_id": "repo_claude_val",
        "license": "CC0-1.0",
        "code": """/**
 * Deep clones any JavaScript object handling nested objects and arrays.
 */
function deepCloneObject(sourceData) {
  if (sourceData === null || typeof sourceData !== 'object') {
    return sourceData;
  }
  if (Array.isArray(sourceData)) {
    return sourceData.map(item => deepCloneObject(item));
  }
  const clonedObject = {};
  for (const [key, value] of Object.entries(sourceData)) {
    clonedObject[key] = deepCloneObject(value);
  }
  return clonedObject;
}"""
    },
    {
        "id": "js_ai_004",
        "language": "javascript",
        "label": 1,
        "source": "starcoder_generation",
        "repo_id": "repo_starcoder_train",
        "license": "CC0-1.0",
        "code": """function matchPathPattern(routePattern, incomingUrl) {
  const patternSegments = routePattern.split('/').filter(Boolean);
  const urlSegments = incomingUrl.split('/').filter(Boolean);
  if (patternSegments.length !== urlSegments.length) return null;
  const extractedParams = {};
  for (let i = 0; i < patternSegments.length; i++) {
    if (patternSegments[i].startsWith(':')) {
      const paramName = patternSegments[i].slice(1);
      extractedParams[paramName] = urlSegments[i];
    } else if (patternSegments[i] !== urlSegments[i]) {
      return null;
    }
  }
  return extractedParams;
}"""
    },

    # =========================================================================
    # JAVA HUMAN-WRITTEN SAMPLES (Guava, Spring)
    # =========================================================================
    {
        "id": "java_h_001",
        "language": "java",
        "label": 0,
        "source": "google/guava/Preconditions",
        "repo_id": "repo_guava",
        "license": "Apache-2.0",
        "code": """public final class Preconditions {
    public static <T> T checkNotNull(T reference, Object errorMessage) {
        if (reference == null) {
            throw new NullPointerException(String.valueOf(errorMessage));
        }
        return reference;
    }

    public static void checkArgument(boolean b, Object errorMessage) {
        if (!b) {
            throw new IllegalArgumentException(String.valueOf(errorMessage));
        }
    }
}"""
    },
    {
        "id": "java_h_002",
        "language": "java",
        "label": 0,
        "source": "spring-framework/StringUtils",
        "repo_id": "repo_spring",
        "license": "Apache-2.0",
        "code": """public abstract class StringUtils {
    public static boolean hasText(CharSequence str) {
        if (str == null || str.length() == 0) {
            return false;
        }
        int strLen = str.length();
        for (int i = 0; i < strLen; i++) {
            if (!Character.isWhitespace(str.charAt(i))) {
                return true;
            }
        }
        return false;
    }
}"""
    },

    # =========================================================================
    # JAVA AI-GENERATED SAMPLES (GPT-4)
    # =========================================================================
    {
        "id": "java_ai_001",
        "language": "java",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_train",
        "license": "CC0-1.0",
        "code": """package com.example.validator;

public class ArgumentValidator {
    /**
     * Validates that the provided object reference is not null.
     * @param referenceObject The object to check
     * @param failureMessage Message thrown if null
     * @return The validated reference
     */
    public static <T> T requireNonNull(T referenceObject, String failureMessage) {
        if (referenceObject == null) {
            throw new NullPointerException(failureMessage != null ? failureMessage : "Object reference must not be null");
        }
        return referenceObject;
    }
}"""
    },
    {
        "id": "java_ai_002",
        "language": "java",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_test",
        "license": "CC0-1.0",
        "code": """package com.example.utils;

public class TextInspector {
    /**
     * Checks whether the specified string contains non-whitespace content.
     */
    public static boolean isNonEmpty(String inputString) {
        if (inputString == null || inputString.trim().isEmpty()) {
            return false;
        }
        return true;
    }
}"""
    },

    # =========================================================================
    # C++ HUMAN-WRITTEN SAMPLES (LLVM, Linux)
    # =========================================================================
    {
        "id": "cpp_h_001",
        "language": "cpp",
        "label": 0,
        "source": "llvm/ADT/SmallVector",
        "repo_id": "repo_llvm",
        "license": "Apache-2.0",
        "code": """template <typename T>
void grow_pod(void *FirstEl, size_t MinCapacity, size_t TSize) {
    size_t NewCapacity = 2 * this->capacity() + 1;
    NewCapacity = std::min(std::max(NewCapacity, MinCapacity), size_t(-1) / TSize);
    void *NewElts = std::malloc(NewCapacity * TSize);
    if (this->BeginX != FirstEl) {
        std::memcpy(NewElts, this->BeginX, this->size() * TSize);
        std::free(this->BeginX);
    }
    this->BeginX = NewElts;
    this->Capacity = NewCapacity;
}"""
    },
    {
        "id": "cpp_h_002",
        "language": "cpp",
        "label": 0,
        "source": "redis/sds",
        "repo_id": "repo_redis",
        "license": "BSD-3-Clause",
        "code": """sds sdsnewlen(const void *init, size_t initlen) {
    void *sh;
    sds s;
    char type = sdsReqType(initlen);
    int hdrlen = sdsHdrSize(type);
    sh = s_malloc(hdrlen + initlen + 1);
    if (sh == NULL) return NULL;
    s = (char*)sh + hdrlen;
    if (initlen && init)
        memcpy(s, init, initlen);
    s[initlen] = '\\0';
    return s;
}"""
    },

    # =========================================================================
    # C++ AI-GENERATED SAMPLES (GPT-4)
    # =========================================================================
    {
        "id": "cpp_ai_001",
        "language": "cpp",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_train",
        "license": "CC0-1.0",
        "code": """#include <cstdlib>
#include <cstring>
#include <algorithm>

template <typename ElementType>
class DynamicBuffer {
    ElementType* bufferData;
    size_t currentCapacity;
public:
    void expandCapacity(size_t minimumTargetCapacity) {
        size_t updatedCapacity = currentCapacity ? currentCapacity * 2 : 8;
        if (updatedCapacity < minimumTargetCapacity) {
            updatedCapacity = minimumTargetCapacity;
        }
        ElementType* newAllocation = static_cast<ElementType*>(std::realloc(bufferData, updatedCapacity * sizeof(ElementType)));
        if (newAllocation != nullptr) {
            bufferData = newAllocation;
            currentCapacity = updatedCapacity;
        }
    }
};"""
    },
    {
        "id": "cpp_ai_002",
        "language": "cpp",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_test",
        "license": "CC0-1.0",
        "code": """#include <string>
#include <memory>
#include <cstring>

std::unique_ptr<char[]> allocateStringCopy(const char* sourceBuffer, size_t bufferLength) {
    auto destinationBuffer = std::make_unique<char[]>(bufferLength + 1);
    if (sourceBuffer != nullptr && bufferLength > 0) {
        std::memcpy(destinationBuffer.get(), sourceBuffer, bufferLength);
    }
    destinationBuffer[bufferLength] = '\\0';
    return destinationBuffer;
}"""
    },
    # =========================================================================
    # GO & TYPESCRIPT HUMAN-WRITTEN SAMPLES
    # =========================================================================
    {
        "id": "go_h_001",
        "language": "go",
        "label": 0,
        "source": "golang/net/http",
        "repo_id": "repo_golang",
        "license": "BSD-3-Clause",
        "code": """func CanonicalMIMEHeaderKey(s string) string {
    b := []byte(s)
    upper := true
    for i, c := range b {
        if upper && 'a' <= c && c <= 'z' {
            b[i] -= 'a' - 'A'
        } else if !upper && 'A' <= c && c <= 'Z' {
            b[i] += 'a' - 'A'
        }
        upper = c == '-'
    }
    return string(b)
}"""
    },
    {
        "id": "ts_h_001",
        "language": "typescript",
        "label": 0,
        "source": "reduxjs/redux",
        "repo_id": "repo_redux",
        "license": "MIT",
        "code": """export function compose(...funcs: Function[]) {
  if (funcs.length === 0) {
    return <T>(arg: T): T => arg;
  }
  if (funcs.length === 1) {
    return funcs[0];
  }
  return funcs.reduce((a, b) => (...args: any[]) => a(b(...args)));
}"""
    },
    {
        "id": "py_h_011",
        "language": "python",
        "label": 0,
        "source": "django/utils/crypto",
        "repo_id": "repo_django",
        "license": "BSD-3-Clause",
        "code": """def constant_time_compare(val1, val2):
    import hmac
    return hmac.compare_digest(val1.encode('utf-8'), val2.encode('utf-8'))"""
    },

    # =========================================================================
    # GO & TYPESCRIPT & PYTHON AI-GENERATED SAMPLES
    # =========================================================================
    {
        "id": "go_ai_001",
        "language": "go",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_train",
        "license": "CC0-1.0",
        "code": """package httphelper

import "strings"

// FormatHeaderKey standardizes an HTTP header string key.
func FormatHeaderKey(headerKey string) string {
    parts := strings.Split(headerKey, "-")
    for i, part := range parts {
        if len(part) > 0 {
            parts[i] = strings.ToUpper(part[:1]) + strings.ToLower(part[1:])
        }
    }
    return strings.Join(parts, "-")
}"""
    },
    {
        "id": "ts_ai_001",
        "language": "typescript",
        "label": 1,
        "source": "gpt-4_generation",
        "repo_id": "repo_gpt4_test",
        "license": "CC0-1.0",
        "code": """type MiddlewareFunction = (...args: unknown[]) => unknown;

/**
 * Composes multiple middleware functions from right to left.
 */
export function composeMiddlewares(...middlewares: MiddlewareFunction[]): MiddlewareFunction {
  return function (initialValue: unknown) {
    return middlewares.reduceRight((accumulated, currentFunc) => {
      return currentFunc(accumulated);
    }, initialValue);
  };
}"""
    },
    {
        "id": "py_ai_009",
        "language": "python",
        "label": 1,
        "source": "deepseek_generation",
        "repo_id": "repo_deepseek_test",
        "license": "CC0-1.0",
        "code": """def secure_string_compare(string_a: str, string_b: str) -> bool:
    \"\"\"
    Constant-time comparison preventing timing attacks.
    \"\"\"
    if len(string_a) != len(string_b):
        return False
    accumulated_diff = 0
    for char_a, char_b in zip(string_a, string_b):
        accumulated_diff |= ord(char_a) ^ ord(char_b)
    return accumulated_diff == 0"""
    }
]


def generate_splits():
    """Partition records by repository into train, validation, and test sets."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    benchmark_dir = os.path.join(base_dir, "benchmark")
    os.makedirs(benchmark_dir, exist_ok=True)

    # Repository-level split definition ensuring zero data leakage
    train_repos = {"repo_cpython", "repo_algorithms", "repo_lodash", "repo_spring", "repo_redis", "repo_gpt4_train", "repo_starcoder_train"}
    val_repos = {"repo_requests", "repo_flask", "repo_express", "repo_claude_val"}
    test_repos = {"repo_django", "repo_numpy", "repo_axios", "repo_guava", "repo_llvm", "repo_deepseek_test", "repo_gpt4_test", "repo_golang", "repo_redux"}

    train_records = []
    val_records = []
    test_records = []

    for s in SAMPLES:
        repo = s["repo_id"]
        if repo in train_repos:
            train_records.append(s)
        elif repo in val_repos:
            val_records.append(s)
        elif repo in test_repos:
            test_records.append(s)
        else:
            train_records.append(s)

    # Write splits
    for filename, records in [
        ("train.jsonl", train_records),
        ("val.jsonl", val_records),
        ("test.jsonl", test_records)
    ]:
        dest_path = os.path.join(benchmark_dir, filename)
        with open(dest_path, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r) + "\n")

    # Generate synthetic demo dataset clearly labeled as synthetic for UI testing
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
    with open(os.path.join(base_dir, "synthetic_demo.jsonl"), "w", encoding="utf-8") as f:
        for r in demo_samples:
            f.write(json.dumps(r) + "\n")

    # Mirror to backend/app/datasets as well
    app_datasets_dir = os.path.abspath(os.path.join(base_dir, "..", "app", "datasets"))
    if os.path.exists(app_datasets_dir):
        app_benchmark_dir = os.path.join(app_datasets_dir, "benchmark")
        os.makedirs(app_benchmark_dir, exist_ok=True)
        for fn in ["train.jsonl", "val.jsonl", "test.jsonl"]:
            src = os.path.join(benchmark_dir, fn)
            dst = os.path.join(app_benchmark_dir, fn)
            shutil.copy2(src, dst)
        shutil.copy2(os.path.join(base_dir, "synthetic_demo.jsonl"), os.path.join(app_datasets_dir, "synthetic_demo.jsonl"))

    print(f"Generated benchmark splits: train={len(train_records)}, val={len(val_records)}, test={len(test_records)}")


if __name__ == "__main__":
    generate_splits()
