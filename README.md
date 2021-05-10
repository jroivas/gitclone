# Gitclone

Simple git clone and sync helper.

Idea of this tool is to automate cloning and updating copies of multiple simple repositories.
In case you want to keep and track some git repositories, this is the tool for you.


## Repositories config

Repositories configuration file is just list of repository URLs and locations in
a text file. Please see [repos.txt.example](repos.txt.example) as an example.

## Usage

Simply provide repositories list, and output directory:

    python gitclone.py -r repos.txt.example -o output_dir sync

This will parse `repost.txt.example` and trying to clone or update every
repository one by one. Output is located in `output_dir`.
