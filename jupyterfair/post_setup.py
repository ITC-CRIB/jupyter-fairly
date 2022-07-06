from pathlib import Path
import random

HERE = Path(__file__).parent.resolve()

# Create directory with dummy files in tests/fixtures/project_example
# This is to ensure that the project is testable
# Make directory in ./tests/fixtures/project_example
DUMMY_PROJECT = "jupyterfair/tests/fixtures/dummy_project"
(HERE / DUMMY_PROJECT).mkdir(parents=True, exist_ok=True)

# Create dummy files in ./tests/fixtures/project_example
def create_file(n, d, path, file_name):
    '''
    Makes a file in the given path containing data with random numbers
    n: number of lines to make
    d: number of characters to make each line
    path: path to make file in
    file_name: name of file to make

    example create a 100 MB file
    create_file(10**5, 100, <target_path>, <file_name>")
    example create a 1 GB file
    create_file(10**6, 100, <target_path>, <file_name>")
    '''
    f = open(f'{path}/{file_name}', 'w')
    for i in range(n):
        nums = [str(round(random.uniform(0, 1000 * 1000), 3)) for j in range(d)]
        f.write(' '.join(nums))
        f.write('\n')
    f.close()

def main():
    '''Generate data to run tests'''
    # Create small file
    create_file(10, 100, HERE / DUMMY_PROJECT, "file_1MB.txt")    

    # Create 10 files of 100 MB each
    for i in range(10):
        create_file(10**5, 100, DUMMY_PROJECT, f'file{i}.txt')

if __name__ == '__main__':
    create_file(10, 100, HERE / DUMMY_PROJECT, "file_1MB.txt")    
    main()
