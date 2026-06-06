from pipeline.model_load import Model

from pipeline.check_diff_files import get_modif_added_files


model_path = 'vuln_model/vulnerability_detector.pkl'
model = Model(model_path)

commit_hash = 'HEAD'  # Always the last commit

for _, file_path in get_modif_added_files(commit_hash):
  print(f'Path: {file_path}')

  with open(file_path) as file:
    code = file.read()

    is_vulnerable, probs = model.predict_code(code)

    print(f'Vulnerable: {is_vulnerable}')
    print(f'Vulnerable Prob: {probs[1]}')
