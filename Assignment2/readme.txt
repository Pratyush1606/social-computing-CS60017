# Assignment 2: Network centrality and community structure

Pratyush Jaiswal  
18EE35014  
Social Computing (CS60017)

------------

## System Requirements

- Python Interpreter used: Python 3.7.9
  The code should run in any version of Python >= 3.7
- networkx 2.6.3
- Jupyter 1.0.0
- Matplotlib

> The dependencies have been frozen inside the requirements.txt file, 
and if you're working in a python virtual environment, the dependencies can be installed using the command  
"pip install -r requirements.txt".

------------

## Folder structure

```
Assignment2
├── datasets
|   ├── football.gml
|   ├── football.txt
|   ├── polbooks.txt
|   ├── polbooks.gml
|   └── imdb_prodco.adj
├── config.py
├── q1.ipynb
├── gen_centrality.py
├── readme.txt
└── requirements.txt
```

- `datasets` folder contains all the data files. So to run the files, please extract the
 data files in this folder with appropiate name
- `q1.ipynb` and `gen_centrality.py` contain all the codes for *question1* and *question2* respectively.
- `config.py` contains all the configurations (paths to datasets and plots)
- `requirements.txt` contains all the dependencies with correct versions.

------------

## Running Instructions

> Use `pip` or `pip3` and `python` or `python3` as per your system configuration for executing the below commands

1. First, change the working directory to this folder

2. It is advised to work inside a virtual environment. Make a virtual environment and activate that.

3. Install all the dependencies
    ```
    pip install -r requirements.txt
    ```

4. * To run *question1*, run all the cells of the `q1.iypnb` file.  
Always use **Run all** command to run the cells of the juputer file. If stopped in between, 
please start running from the starting cell otherwise duplicate outputs will be genrated into the output files.
  
   * To run *question2*, run `gen_centrality.py` file.
 
     ```
     python gen_centrality.py
     ```

------------

## Points to Consider

* After successful execution of the above files, a folder `PLOT` containing all the
specific distribution plots and other *txt* files containing all the answers of both the 
questions will be generated.

* **While running *q1.ipynb*, if it is stopped in between the execution, please run the
 file again from the starting cell otherwise the duplicate outputs will get appended into
 the output files.**
