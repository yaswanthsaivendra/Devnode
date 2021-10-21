# Devnode
A website to bring together Techies of SVNIT to form a dev community.

Make sure u have python3 installed.
Then install the virtualenv using
```
pip install virtualenv
```

## Setup
If the current repo consists of env folder, first delete it before creating a new one in 2nd step below.
1. Step 1 :
```
git clone repo_url
cd repo_name
```
2. Create a virtualenv :
```
virtualenv env
```
3. Activate the virtual environment.
```
source ./env/bin/activate
```
4. Install the requirements
```
pip install -r requirements.txt
```
5. Run the server
```
python3 run.py
```

*Note*
1. In windows, the above 3rd command is replaced by
```
env\Scripts\activate
```

Incase if u want to deactivate ur virtual environment, use
`deactivate`

Navigate to `http://127.0.0.1:5000/`