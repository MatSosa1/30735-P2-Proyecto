import os

import pipeline.exceptions as exc
from pipeline.model_load import Model
from pipeline.check_diff_files import get_modif_added_files


model_path = 'vuln_model/vulnerability_detector.pkl'
model = Model(model_path)

base_hash = os.environ['BASE_SHA']
commit_hash = os.environ['HEAD_SHA']

for _, file_path in get_modif_added_files(base_hash, commit_hash):
  print(f'Path: {file_path}')

  if not os.path.exists(file_path):
    raise exc.CodeFileNotFoundError(f'No se ha encontrado el archivo {file_path}')

  with open(file_path) as file:
    code = file.read()

    is_vulnerable, probs = model.predict_code(code)

    print(f'Vulnerable: {is_vulnerable}')
    print(f'Vulnerable Prob: {probs[1]}')

    if is_vulnerable:
      raise exc.VulnerableCommitError(f'El modelo ha detectado vulnerabilidades en el código modificado con {probs[1] * 100}% de probabilidad')
