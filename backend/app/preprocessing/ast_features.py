"""
AST-based structural feature extraction for code authorship analysis.
Uses Python's native AST parser with robust heuristic fallbacks for
syntax errors and non-Python languages.
"""

import ast
from typing import Dict, Any, List


class ASTFeatureExtractor:
    """Extracts structural AST metrics for deep learning and feature fusion."""

    def __init__(self):
        pass

    def _get_tree_depth(self, node: ast.AST, current_depth: int = 1) -> int:
        """Calculate maximum tree depth of an AST."""
        max_d = current_depth
        for child in ast.iter_child_nodes(node):
            d = self._get_tree_depth(child, current_depth + 1)
            if d > max_d:
                max_d = d
        return max_d

    def extract_python_ast(self, code: str) -> Dict[str, float]:
        """Extract deep AST metrics from valid Python code."""
        try:
            tree = ast.parse(code)
        except (SyntaxError, ValueError):
            return self.extract_fallback(code)

        total_nodes = 0
        depth = self._get_tree_depth(tree)
        control_flow_count = 0
        function_count = 0
        class_count = 0
        expr_count = 0
        name_count = 0
        arg_counts: List[int] = []
        comprehensions = 0
        returns = 0

        for node in ast.walk(tree):
            total_nodes += 1
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.Match if hasattr(ast, 'Match') else ast.If)):
                control_flow_count += 1
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_count += 1
                arg_counts.append(len(node.args.args))
            elif isinstance(node, ast.ClassDef):
                class_count += 1
            elif isinstance(node, ast.Expr):
                expr_count += 1
            elif isinstance(node, ast.Name):
                name_count += 1
            elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
                comprehensions += 1
            elif isinstance(node, ast.Return):
                returns += 1

        denom = max(1, total_nodes)
        avg_args = float(sum(arg_counts) / len(arg_counts)) if arg_counts else 0.0

        return {
            "ast_node_count": float(total_nodes),
            "ast_max_depth": float(depth),
            "ast_control_flow_count": float(control_flow_count),
            "ast_function_count": float(function_count),
            "ast_class_count": float(class_count),
            "ast_branch_density": float(control_flow_count / denom),
            "ast_expr_density": float(expr_count / denom),
            "ast_identifier_density": float(name_count / denom),
            "ast_comprehension_ratio": float(comprehensions / denom),
            "ast_avg_function_args": avg_args,
            "ast_return_density": float(returns / denom),
        }

    def extract_fallback(self, code: str) -> Dict[str, float]:
        """Heuristic proxy for non-Python or unparseable code."""
        lines = [l for l in code.split("\n") if l.strip()]
        line_count = max(1, len(lines))
        
        # Estimate depth via brace / indentation nesting
        max_depth = 1
        curr_depth = 1
        control_flow = 0
        functions = 0
        classes = 0
        
        control_keywords = {"if", "else", "for", "while", "switch", "case", "catch", "try", "match"}
        
        for line in lines:
            stripped = line.strip()
            # Indent / brace tracking
            open_braces = stripped.count("{") + stripped.count("(")
            close_braces = stripped.count("}") + stripped.count(")")
            curr_depth = max(1, curr_depth + open_braces - close_braces)
            max_depth = max(max_depth, curr_depth)
            
            words = stripped.split()
            if any(w in control_keywords for w in words):
                control_flow += 1
            if any(w in {"def", "function", "fn", "func"} or "=>" in stripped for w in words):
                functions += 1
            if any(w in {"class", "struct", "interface"} for w in words):
                classes += 1

        est_nodes = line_count * 4
        return {
            "ast_node_count": float(est_nodes),
            "ast_max_depth": float(max(max_depth, 3)),
            "ast_control_flow_count": float(control_flow),
            "ast_function_count": float(functions),
            "ast_class_count": float(classes),
            "ast_branch_density": float(control_flow / max(1, est_nodes)),
            "ast_expr_density": 0.25,
            "ast_identifier_density": 0.35,
            "ast_comprehension_ratio": 0.02,
            "ast_avg_function_args": 1.5,
            "ast_return_density": float(functions / max(1, est_nodes)),
        }

    def extract(self, code: str, language: str = "python") -> Dict[str, float]:
        if language.lower() in ("python", "py"):
            return self.extract_python_ast(code)
        return self.extract_fallback(code)
