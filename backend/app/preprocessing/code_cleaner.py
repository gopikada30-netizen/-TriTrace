"""
Code cleaning, normalization, and controlled syntactic transformation utilities
for TriTrace robustness analysis and input sanitization.
"""

import re
import tokenize
import io
from typing import List, Tuple, Dict, Any


def normalize_code(code: str) -> str:
    """Normalize line breaks and trailing spaces."""
    if not code:
        return ""
    lines = code.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "\n".join(line.rstrip() for line in lines)


def strip_comments_and_docstrings(code: str, language: str = "python") -> str:
    """Remove comments and docstrings while preserving semantic code structure."""
    if not code.strip():
        return ""

    if language.lower() in ("python", "py"):
        try:
            tokens = tokenize.generate_tokens(io.StringIO(code).readline)
            result = []
            prev_toktype = tokenize.INDENT
            
            for tok in tokens:
                token_type = tok.type
                token_string = tok.string
                
                # Filter out comments
                if token_type == tokenize.COMMENT:
                    continue
                # Filter out docstrings
                if token_type == tokenize.STRING:
                    if prev_toktype in (tokenize.INDENT, tokenize.NL, tokenize.NEWLINE) and (
                        token_string.startswith('"""') or token_string.startswith("'''")
                    ):
                        continue
                
                result.append((tok.exact_type if hasattr(tok, 'exact_type') else token_type, token_string))
                prev_toktype = token_type
            
            lines = code.split("\n")
            cleaned_lines = []
            in_multiline = False
            quote_char = None
            
            for line in lines:
                sline = line.strip()
                if not in_multiline:
                    if sline.startswith('"""') or sline.startswith("'''"):
                        quote_char = sline[:3]
                        if sline.count(quote_char) >= 2 and len(sline) > 3:
                            continue  # Single-line docstring
                        in_multiline = True
                        continue
                    if sline.startswith("#"):
                        continue
                    # Strip inline comments if not inside quotes
                    if "#" in line:
                        parts = line.split("#", 1)
                        if parts[0].count('"') % 2 == 0 and parts[0].count("'") % 2 == 0:
                            line = parts[0]
                    cleaned_lines.append(line)
                else:
                    if quote_char in sline:
                        in_multiline = False
                        quote_char = None
                    continue
            return "\n".join(cleaned_lines)
        except Exception:
            # Fallback regex removal
            code_no_comments = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
            return code_no_comments
    else:
        # C/Java/JS style comments
        cleaned = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        cleaned = re.sub(r'/\*[\s\S]*?\*/', '', cleaned)
        return cleaned


def rename_identifiers(code: str, language: str = "python") -> Tuple[str, Dict[str, str]]:
    """Controlled identifier obfuscation for robustness evaluation.
    Replaces variable/function names with standardized identifiers (var_1, var_2, ...).
    """
    python_keywords = {
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
        'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
        'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
        'self', 'cls', 'int', 'str', 'float', 'bool', 'list', 'dict', 'set', 'tuple',
        'print', 'len', 'range', 'enumerate', 'zip', 'open', 'type', 'isinstance'
    }
    
    tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
    mapping = {}
    counter = 1
    
    for t in tokens:
        if t not in python_keywords and not t.startswith("__"):
            if t not in mapping:
                mapping[t] = f"var_{counter}"
                counter += 1
                
    modified_code = code
    # Sort keys by length descending to avoid partial word replacements
    for original, replacement in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = r'\b' + re.escape(original) + r'\b'
        modified_code = re.sub(pattern, replacement, modified_code)
        
    return modified_code, mapping


def perturb_whitespace(code: str, style: str = "compact") -> str:
    """Modify indentation and blank lines to test formatting robustness."""
    lines = code.split("\n")
    if style == "compact":
        # Remove empty lines and trailing whitespace
        return "\n".join(line for line in lines if line.strip())
    elif style == "spaced":
        # Double empty lines between non-empty lines
        spaced = []
        for line in lines:
            spaced.append(line)
            if line.strip().endswith(":") or line.strip().endswith("{"):
                spaced.append("")
        return "\n".join(spaced)
    elif style == "indent_tabs":
        # Convert 4 spaces to tabs
        return "\n".join(re.sub(r'^( {4})+', lambda m: '\t' * (len(m.group(0)) // 4), line) for line in lines)
    return code


def apply_safe_refactoring(code: str, language: str = "python") -> Tuple[str, Dict[str, Any]]:
    """
    Apply safe, semantics-preserving refactoring patterns.
    - Normalizes equality/identity checks (e.g., '== True', '!= None')
    - Standardizes augmented assignments (e.g., 'x = x + 1' -> 'x += 1')
    - Normalizes boolean inversion logic
    Returns: (refactored_code, refactoring_metadata)
    """
    if language.lower() not in ("python", "py"):
        return code, {
            "applied": False,
            "transformations_count": 0,
            "supported": False,
            "details": f"Safe AST refactoring currently supports Python. Given: {language}"
        }

    transformations = []
    refactored = code

    # Pattern 1: x = x + 1 -> x += 1
    aug_assign_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*\1\s*([+\-*/%])\s*([a-zA-Z0-9_]+)'
    if re.search(aug_assign_pattern, refactored):
        refactored = re.sub(aug_assign_pattern, r'\1 \2= \3', refactored)
        transformations.append("Standardized explicit assignment into augmented operator (e.g. x += 1)")

    # Pattern 2: if x == True: -> if x:
    if re.search(r'\bif\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*==\s*True\s*:', refactored):
        refactored = re.sub(r'\bif\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*==\s*True\s*:', r'if \1:', refactored)
        transformations.append("Simplified redundant boolean comparison '== True'")

    # Pattern 3: if x == False: -> if not x:
    if re.search(r'\bif\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*==\s*False\s*:', refactored):
        refactored = re.sub(r'\bif\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*==\s*False\s*:', r'if not \1:', refactored)
        transformations.append("Simplified boolean comparison '== False' to 'not'")

    # Pattern 4: x != None -> x is not None
    if re.search(r'\b!=\s*None\b', refactored):
        refactored = re.sub(r'\s*!=\s*None\b', ' is not None', refactored)
        transformations.append("Standardized equality check to identity check 'is not None'")

    # Pattern 5: x == None -> x is None
    if re.search(r'\b==\s*None\b', refactored):
        refactored = re.sub(r'\s*==\s*None\b', ' is None', refactored)
        transformations.append("Standardized equality check to identity check 'is None'")

    applied = len(transformations) > 0
    return refactored, {
        "applied": applied,
        "transformations_count": len(transformations),
        "supported": True,
        "transformations": transformations if applied else ["No matching refactoring idioms detected in snippet."]
    }
