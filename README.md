# Create Introductions Issues

<!--start-->
Create GitHub issues for all introductions tasks.

## Requirements

- GitHub CLI
- Conda (Anaconda or MiniConda)

## Getting Started

### 1 - Clone this repo.

### 2 - Create the contacts CSV file.
    - location: `./data/raw/contacts.csv`
    - columns: `name`, `role`
    - contents: Name of each person, and their title or role description.

!!! note
    This file will not be included in Git version control. Everything in the `./data` directory is excluded using `.gitignore`.

### 3 - Set repo properties.

Set the following variables in `./scripts/config.py`.

```
github_owner = "your_glorious_self"
github_repo = "personal-issues"
```

### 4 - Create a Python Conda environment with the requirements.
    
```
make env
```

This makes a Conda environment in `./env` with dependencies listed in the `./envornment.yml` file. This includes more than
just the minimum required to run the project. It incldues the requirements to build the documentation as well.

If all you want to do is run this project, you can easily run the following commands in an enviroment with Conda available
from the root of the project. This will create a Conda environment in `./env` and install the local project so logging will
work as expected.

```
conda create -p ./env
conda activate -p ./env
pip install -e .
```

4 - Explore and Experiment
  
This repo is was created using the [Cookiecutter-Spatial-Data-Science](https://github.com/knu2xs/cookiecutter-spatial-data-science) 
template. The only thing being used from the templated project package is `get_logger`. Otherwise, all the processing logic is in 
`scripts/make_introduction_logic.py`.

<!--end-->

<p><small>Project based on the <a target="_blank" href="https://github.com/knu2xs/cookiecutter-spatial-data-science">cookiecutter 
Spatial Data Science project template</a>. This template, in turn, is simply an extension and light modification of the 
<a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project 
template</a>. #cookiecutterdatascience</small></p>
