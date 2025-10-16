# Prime
> Execute the following sections to understand the codebase then summarize your understanding.

## Read
.env.sample (never read .env)
./app/tws/.env.sample (never read .env)
./app/backend/.env.sample (never read .env)
README.md
adws/README.md
.claude/commands/util/conditional_docs.md - this is a guide for you to determine which documentation to read based on the upcoming task.

## Run
- git ls-files
- Think through each of these steps to make sure you don't miss anything
- Initialize a new uv virtual environment for python development if it does not exist
- Install dependencies
- Check if python package is installed
  - If not installed, run `./.claude/scripts/install_ibapi.sh` to install tws ibapi
- Create a `./specs` folder in the root directory if it does not exist
  - Under the `./specs` folder, create 4 subfolders:
    - `chores`
    - `features`
    - `bugs`
    - `patches`

- Create a `./app` folder in the root directory if it does not exist
  - Under the `./app` folder, create 3 subfolders:
    - `tws`
    - `backend`
    - `frontend`


## Report
- Output the work you've just done in a concise bullet point list.
- Instruct the user to fill out the root level ./.env based on .env.sample. 
- If `./app/backend/.env` does not exist, instruct the user to fill out `./app/backend/.env` based on `./app/server/.env.sample`
- If `./env` does not exist, instruct the user to fill out `./env` based on `./env.sample`
- Mention: 'To setup your AFK Agent, be sure to update the remote repo url and push to a new repo so you have access to git issues and git prs:
  ```
  git remote add origin <your-new-repo-url>
  git push -u origin main
  ```'
- Mention: If you want to upload images to github during the review process setup cloudflare for public image access you can setup your cloudflare environment variables. See .env.sample for the variables.