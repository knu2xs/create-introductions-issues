from datetime import datetime
from pathlib import Path
import importlib.util
import subprocess
import sys

import pandas as pd
import requests

# path to the root of the project
dir_prj = Path(__file__).parent.parent


def get_github_token() -> str | None:
    """Retrieve GitHub token using gh CLI."""
    try:
        # Run the gh command to get the token
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True
        )
        token = result.stdout.strip()
        return token
    except subprocess.CalledProcessError as e:
        print("Error retrieving token:", e)
        return None
    

def create_issue(title: str, body: str, labels: list[str]) -> int | None:
    """Create an issue."""
    payload = {
        "title": title,
        "body": body,
        "labels": labels
    }
    response = requests.post(BASE_URL, headers=headers, json=payload)
    if response.status_code == 201:
        issue = response.json()
        logger.info(f"Issue created: {issue['html_url']}")
        return issue['number']
    else:
        logger.error(f"Error creating issue: {response.status_code} {response.text}")
        return None
    

def add_subissue_to_parent(parent_issue_number: int, subissue_number: int) -> None:
    """Add a sub-issue link to the parent issue."""
    # get the ID for the subissue
    id_url = f"{BASE_URL}/{subissue_number}"
    response = requests.get(id_url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Error retrieving subissue issue ID: {response.status_code} {response.text}")
        return
    subissue = response.json()
    subissue_id = subissue['id']

    # Construct the URL for adding a sub-issue
    url = f"{BASE_URL}/{parent_issue_number}/sub_issues"

    # Payload to link the sub-issue
    payload = {
        "sub_issue_id": int(subissue_id) if not isinstance(subissue_id, int) else subissue_id
    }
    
    # Make the API request to link the sub-issue
    response = requests.post(url, headers=headers, json=payload)

    # Check the response status code and log accordingly
    if response.status_code == 200:
        logger.info(f"Sub-issue #{subissue_number} linked to parent issue #{parent_issue_number}")
    else:
        logger.error(f"Error linking sub-issue: {response.status_code} {response.text}")


# if the project package is not installed in the environment
if importlib.util.find_spec('create_introductions_issues') is None:
    
    # get the relative path to where the source directory is located
    src_dir = dir_prj / 'src'

    # throw an error if the source directory cannot be located
    if not src_dir.exists():
        raise EnvironmentError('Unable to import create_introductions_issues.')

    # add the source directory to the paths searched when importing
    sys.path.insert(0, str(src_dir))

# import create_introductions_issues
from create_introductions_issues.utils import get_logger

# import configuration variables
from config import log_level, github_owner, github_repo, meeting_agenda_template

# repo url
BASE_URL = f"https://api.github.com/repos/{github_owner}/{github_repo}/issues"

# get datestring for file naming yyyymmddThhmmss
date_string = datetime.now().strftime("%Y%m%dT%H%M%S")

# paths
dir_data = dir_prj / 'data'
log_dir = dir_data / 'logs'
poc_csv = dir_data / 'raw' / 'contacts.csv'

if not log_dir.exists():
    log_dir.mkdir(parents=True)

log_file = log_dir / f'{Path(__file__).stem}_{date_string}.log'

# use the log level from the config to set up logging
logger = get_logger(level=log_level, logfile_path=log_file)

# read the csv file containing the points of contact
poc_df = pd.read_csv(poc_csv, header=0)

# log reading the points of contact
logger.info(f'Read {len(poc_df)} points of contact from {poc_csv.absolute()}')

logger.info(f'Starting to create issues in {github_repo}')

# Get token from gh CLI
import subprocess
token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()

# Set up headers for authentication
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json"
}

# create parent issue for introductions
epic_issue_number = create_issue(
    title="Professional Networking Introductions",
    body="Networking introductions to facilitate professional connections in Professional Services.",
    labels=["epic", "introductions"]
)

# iterate over points of contact and create issues
for index, row in poc_df.iterrows():
    name = row['name']
    role = row['role']
    
    # create main task issue for the point of contact
    title = f"Introduction: {name} - {role}"
    body = f"Connect with _{name}_, who is a _{role}_ in Professional Services.\n\n{meeting_agenda_template}"
    labels = ["task", "introductions"]

    # create the main task issue
    task_issue_number = create_issue(title, body, labels)

    # if issue creation was successful
    if task_issue_number:

        logger.info(f"Issue #{task_issue_number} created for {name}")
        
        # link task issue to epic issue
        add_subissue_to_parent(epic_issue_number, task_issue_number)

    else:
        logger.error(f"Failed to create issue for {name}")
