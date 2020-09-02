import subprocess


if __name__ == '__main__':
    subprocess.run(["python", "0_combine.py", "--no-sampling"])
    subprocess.run(["python", "1_preprocessing.py"])
    subprocess.run(["python", "2_kss.py"])
    # subprocess.run(["python", "3_clean.py"])
