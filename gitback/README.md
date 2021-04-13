README
======================================

This is a simple utility to backup all the repositories in your GitHub organization. 

Dependencies
======================================
python 3

How to use
======================================
Use the below command manually or in an automated fashion to get the backups.

> python3 -m gitback -o <your_github_orgname> -d git_backup -t <base64_encoded_github_pat> --shallow

Use your github organization name for the -o argument above. This can be obtained from the github URL of your github account immediately followed by the https://github.com/
Use the base64 encoded github personal access token (PAT) as the authentication credential for the -t arguument above. Use below link to learn how to generate a PAT.

https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

Output
======================================
This will create a folder called git_backup in the current folder for cloning all git repos followed by a dated archive folder to archive adaily backups in tar.gz format.
