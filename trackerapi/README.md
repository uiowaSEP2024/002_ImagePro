# trackerapi
TrackerAPI is a wrapper library around the HTTP endpoints for the `backend` service.


# Example
For an example of how TrackerAPI can be used, see and example job script in `demo/mockscript.py`.

In the `mockscript.py` example, it communicates with a locally running `backend`. 
> See the [`backend` README](https://github.com/sep-23/team_03/tree/main/backend#readme) for how to set up and start your backend locally.

To run this example, from the `trackerapi` directory, run the following command in your terminal
```bash
python -m demo.mockscript
```

# Usage

## Scripts

### `trackerapi.generate_json_schemas`
The `trackerapi` has a script for generating the JSON schema for job configurations.

```bash
python -m trackerapi.generate_json_schemas <destination-directory>
```
**Result**
```text
Generated JSON Schema for JobConfigs at <destination-directory>
```

For the script's manual, run:
```bash
python -m trackerapi.generate_json_schemas -h
```
**Output**
```txt
usage: generate_json_schemas.py [-h] [-n NAME] location

positional arguments:
  location              Location of generated schemas

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name to use for the generated <name>.generated.json schema file
```