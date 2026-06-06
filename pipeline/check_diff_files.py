import subprocess

def get_modif_added_files(commit_hash):
  dev_code_path = 'src/'

  output = subprocess.run(
    ["git", "diff-tree", "--no-commit-id", "--name-status", "-r", commit_hash],
    capture_output=True,
    text=True,
    check=True
  )

  files = [line.split('\t')[:2] for line in output.stdout.strip().split('\n')]

  return [file for file in files if file[0] != 'D' and file[1].startswith(dev_code_path)]  # No deleted files
