import subprocess

def get_modif_added_files(base_sha, head_sha):
  dev_code_path = 'src/'

  output = subprocess.run(
    [
      'git',
      'diff',
      '--name-status',
      base_sha,
      head_sha
    ],
    capture_output=True,
    text=True,
    check=True
  )

  files = [
    line.split('\t')[:2]
    for line in output.stdout.splitlines()
  ]

  filtered_files = []

  for file in files:
    # No deleted files
    if file[0] != 'D' and file[1].startswith(dev_code_path):
      filtered_files.append(file)

  return filtered_files