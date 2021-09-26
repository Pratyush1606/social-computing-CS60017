# Assignment 1: Measuring network structure

Pratyush Jaiswal  
18EE35014  
Social Computing (CS60017)

------------

## System Requirements

- Python Interpreter used: Python 3.7.9
  The code should run in any version of Python >= 3.6
- SNAP 6.0.0
- Pillow 8.3.2

> The dependencies have been frozen inside the requirements.txt file, and if you're working in a python virtual environment, the dependencies can be installed using the command  
"pip install -r requirements.txt".

## Folder structure

```
Assignment1
├── datasets
|   ├── Email-EuAll.txt
|   ├── email-EuAll.txt.gz
|   ├── facebook_combined.txt.gz
|   └── facebook_combined.txt
├── config.py
├── log.txt
├── q1.py
├── q2.py
├── run_assignment.py
├── readme.txt
└── requirements.txt
```

- `datasets` folder contains all the data files.
- `q1.py` and `q2.py` contain all the codes for question1 and question2 respectively.
- `config.py` contains all the configurations (paths to datasets and plots)
- `run_assignment.py` runs both `q1.py` and `q2.py` and generates `answers.txt` with the outputs of both the questions.  

  To run the individual question, use the command like `python q1.py` but it will override the `answers.txt` with the output of only this question.

- `requirements.txt` contains all the dependencies with correct versions.
- `logs.txt` contains the outputs obtained while running

## Running Instructions

> Use `pip` or `pip3` and `python` or `python3` as per your system configuration for executing the below commands

1. First, change the working directory to this folder

2. It is advised to work inside a virtual environment. Make a virtual environment and activate that.

3. Install all the dependencies
    ```
    pip install -r requirements.txt
    ```

4. Make sure `gnuplot` is installed on the system and is added to the PATH. This is used by `SNAP` module to generate the plots.

5. Run `run_assignment.py`
    ```
    python run_assignment.py
    ```

After successful execution of the above command, a folder `plots` containing all the specific distribution plots and `answers.txt` containing all the answers of both the questions will be generated.

The output will be generated inside the file `answers.txt` and will be printed to STDOUT also.

During the above execution, some intermediate plot files of extension .png, .plt and .tab will be generated inside this directory. Then the correct plot file will be moved/saved to `plots` folder, and the rest files (of extension .plt and .tab, also .png in case of the second question as it is asked to save in .jpg format) will be deleted. At the ned of the execution, all the specified plots with correct names and extensions will have been generated in `plots`.
