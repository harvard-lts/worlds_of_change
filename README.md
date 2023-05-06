# Worlds of Change Scripts

These scripts are designed to retrieve transcript files from the 
[FromThePage](https://fromthepage.com/) service and structure the retrieved
files to be bulk-ingested into the DRS.
The tool takes a DRS Object ID as input and retrieves the transcripts for all
of the images associated with that Object.

## Installation

1. Clone this repository
   ```
   git clone https://github.com/harvard-lts/worlds_of_change.git
   ```

1. Configure DRS DB credentials.
Copy the 'example.env' to '.env' and populate username and password

### Run on computer locally

Install the dependency modules and install Oracle manually.

1. Install dependency modules
   ```
   cd worlds_of_change
   pip install -r requirements.txt
   ```
  
1. Install Oracle library, see [docs](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html).
Download "Oracle Instant Client" and note the directory of the unzipped binaries, the location will need to be passed into the script if not found at the default location: './instantclient_19_8'

## Unit tests
1. To execute unit tests, run:
   ```
   python -m pytest tests/unit
   ```

## Integration tests (requires read-only .env credentials, and Harvard VPN)
1. To execute unit tests, run:
   ```
   python -m pytest tests/integration
   ```

## Run the script
To see the help documentation:
```
export PYTHONPATH=%{PYTHONPATH}:src
python src/woc/main.py -h
```

Example run (with DRS Object ID of '460390368' and staging directory of
 'output' in the 'prod' environment):
```
python src/woc/main.py -o 460390368 -s output -e prod
```
