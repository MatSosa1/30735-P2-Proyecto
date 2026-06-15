import re

PATTERNS = [
  (r'\b(gets|strcpy|strcat|sprintf|memcpy)\s*\(', 'CWE-120 Buffer Overflow'),
  (r'\beval\s*\(|\bexec\s*\(', 'CWE-95 Code Injection'),
  (r'\b(os\.system|subprocess\.\w+\([^)]*shell\s*=\s*True|system|popen)\s*\(', 'CWE-78 OS Command Injection'),
  (r'(SELECT|INSERT|UPDATE|DELETE)\b.*(\+|%s|%d|\.format\(|f["\'])', 'CWE-89 SQL Injection'),
  (r'\b(pickle\.loads?|yaml\.load)\s*\(', 'CWE-502 Deserialization'),
  (r'\b(md5|sha1)\s*\(', 'CWE-327 Weak Cryptography'),
  (r'(\.\./|\.\.\\)', 'CWE-22 Path Traversal'),
  (r'(password|passwd|secret|api_?key|token)\s*=\s*["\'][^"\']+["\']', 'CWE-798 Hardcoded Credentials'),
]


def infer_vuln_type(code):
  for pattern, label in PATTERNS:
    if re.search(pattern, code, re.IGNORECASE):
      return label

  return 'Vulnerabilidad genérica (tipo no determinado)'