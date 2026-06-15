import os

import pipeline.exceptions as exc
from pipeline.model_load import Model
from pipeline.vuln_type import infer_vuln_type
from pipeline.check_diff_files import get_modif_added_files


def write_github_output(result, probability, file_path, vuln_type):
  output_path = os.environ.get('GITHUB_OUTPUT')

  if not output_path:
    return

  with open(output_path, 'a') as output:
    output.write(f'result={result}\n')
    output.write(f'probability={probability:.4f}\n')
    output.write(f'file={file_path}\n')
    output.write(f'vuln_type={vuln_type}\n')


model_path = 'vuln_model/vulnerability_detector.pkl'
model = Model(model_path)

base_hash = os.environ['BASE_SHA']
commit_hash = os.environ['HEAD_SHA']

any_vulnerable = False
max_prob = 0.0
affected_file = ''
vuln_type = ''

for _, file_path in get_modif_added_files(base_hash, commit_hash):
  print(f'Path: {file_path}')

  if not os.path.exists(file_path):
    raise exc.CodeFileNotFoundError(f'No se ha encontrado el archivo {file_path}')

  with open(file_path) as file:
    code = file.read()

    is_vulnerable, probs = model.predict_code(code)
    vuln_prob = probs[1]

    print(f'Vulnerable: {is_vulnerable}')
    print(f'Vulnerable Prob: {vuln_prob}')

    if vuln_prob >= max_prob:
      max_prob = vuln_prob
      affected_file = file_path

    if is_vulnerable:
      any_vulnerable = True
      vuln_type = infer_vuln_type(code)

result = 'VULNERABLE' if any_vulnerable else 'SEGURO'

write_github_output(result, max_prob, affected_file, vuln_type)

if any_vulnerable:
  raise exc.VulnerableCommitError(
    f'El modelo ha detectado vulnerabilidades en el código modificado con {max_prob * 100}% de probabilidad'
  )