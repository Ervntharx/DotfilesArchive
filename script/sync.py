import sys
import os
import yaml
from pathlib import Path
import subprocess

# get cli args
args = sys.argv

yaml_path = None
bak_path = None

for i in range(1, len(args)-1):
    if args[i] == "--dotfiles-refer":
        yaml_path = args[i+1]
    elif args[i] == "--dotfiles-source":
        bak_path = args[i+1]

if not yaml_path or not bak_path:
    print("err:\tlack config path and dotfiles data source")
    sys.exit(1)

# read files path in config
with open(Path(yaml_path), "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
    dotfiles_path:list[str] = data.get("track_list", [])

# statistics
probe_files_count = 0
copy_task_count = 0
success_count = 0
fail_count = 0

for file_path in dotfiles_path:
    # get full pathes of bak files
    print("<msg>: probe file...", end = "\t")
    ls_cmd: str = f"ls -d {file_path.replace(" ", "\\ ")}"
    process_result: subprocess.CompletedProcess[str] = subprocess.run(ls_cmd,shell=True,capture_output=True, text=True)
    if process_result.returncode != 0:
        print(f"fail!\n{process_result.stderr}\tcontinue to next...")
        fail_count += 1
        continue
    source_path_ls:list[str] = process_result.stdout.strip().split("\n")

    probe_files_count += len(source_path_ls)
    print("success! found files:",*source_path_ls, sep="\n")

    for source_path in source_path_ls:
        copy_task_count += 1

        # produce full target path to restore
        target_path = os.path.abspath(bak_path) + source_path

        # mkdir
        print(f"<msg> try to mkdir...", end="\t")

        mkdir_cmd = f"mkdir -p \"$(dirname '{target_path}')\""
        process_result = subprocess.run(mkdir_cmd, shell=True, capture_output=True, text= True)
        if(process_result.returncode != 0):
            print(f"fail!\n{process_result.stderr}\tcontinue to next...")
            fail_count += 1
            continue

        # copy files
        cp_cmd = f"cp -r \"{source_path}\" \"{target_path}\""

        print(f"<msg>: start copy '{source_path}' to '{target_path}'...", end="\t")

        process_result = subprocess.run(cp_cmd, shell= True,capture_output=True, text=True )
        if(process_result.returncode!=0):
            print(f"fail!\n{process_result.stderr}\tcontinue to next...")
            fail_count += 1
            continue

        success_count +=1
        print("done!")
        
print(f"<msg>\ttask completed with {success_count} success, {fail_count} fail in {copy_task_count} tasks and {probe_files_count} files")



