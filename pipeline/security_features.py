import re

import numpy as np
from scipy import sparse
from sklearn.base import BaseEstimator, TransformerMixin

VULN_PATTERNS = [
  r'\beval\s*\(',
  r'\bexec\s*\(',
  r'\bos\.system\s*\(',
  r'\bos\.popen\s*\(',
  r'subprocess\.\w+\([^)]*shell\s*=\s*True',
  r'\bsystem\s*\(',
  r'\b(pickle\.loads?|cPickle\.loads?)\s*\(',
  r'\byaml\.load\s*\(',
  r'\b(md5|sha1)\s*\(',
  r'\b(gets|strcpy|strcat|sprintf|memcpy)\s*\(',
  r'(SELECT|INSERT|UPDATE|DELETE)\b[^;\n]*(\+|\.format\s*\(|f["\'])',
  r'\.innerHTML\s*=',
  r'document\.write\s*\(',
  r'(\.\./|\.\.\\)',
  r'os\.path\.join\s*\(',
  r'(password|passwd|secret|api_?key|token)\s*=\s*["\'][^"\']+["\']',
]

SAFE_PATTERNS = [
  r'execute\s*\([^)]*,\s*[\(\[]',
  r'\?\s*[,\)]',
  r'\b(bcrypt|scrypt|argon2|pbkdf2)\b',
  r'\b(escape|sanitize|htmlspecialchars|quote)\s*\(',
  r'os\.path\.basename\s*\(',
  r'\b(realpath|abspath)\s*\(',
  r'(preparedstatement|preparestatement|setstring)',
  r'subprocess\.(run|call|Popen)\s*\(\s*\[',
  r'%s["\']?\s*,',
]

_VULN_RE = [re.compile(p, re.IGNORECASE) for p in VULN_PATTERNS]
_SAFE_RE = [re.compile(p, re.IGNORECASE) for p in SAFE_PATTERNS]


def _nesting_depth(code):
  depth = max_depth = 0
  for ch in code:
    if ch in '([{':
      depth += 1
      if depth > max_depth:
        max_depth = depth
    elif ch in ')]}':
      depth = max(0, depth - 1)

  indent_depth = 0
  for line in code.split('\n'):
    stripped = line.lstrip(' ')
    if stripped:
      indent_depth = max(indent_depth, (len(line) - len(stripped)) // 4)

  return max(max_depth, indent_depth)


class SecurityFeatures(BaseEstimator, TransformerMixin):
  def __init__(self, scale=1.0):
    self.scale = scale

  def fit(self, X, y=None):
    return self

  def transform(self, X):
    rows = []
    for code in X:
      code = code if isinstance(code, str) else str(code)
      feats = [self.scale if r.search(code) else 0.0 for r in _VULN_RE]
      feats += [self.scale if r.search(code) else 0.0 for r in _SAFE_RE]
      feats.append(min(len(code) / 1000.0, 5.0))
      feats.append(min(_nesting_depth(code) / 3.0, 5.0))
      rows.append(feats)

    return sparse.csr_matrix(np.array(rows, dtype=np.float64))
