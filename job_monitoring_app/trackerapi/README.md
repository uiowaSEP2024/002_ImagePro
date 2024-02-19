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

## API Usage

### Prerequisites
Before using `trackerapi`, you would need to have already defined a job or process which you would want to track
progress for.

For this section, we will take a job that has the following basic steps:
1. Say "Hello `<name>`"
2. Generate a random number
3. Say "Bye `<name`"

Here is what such a script could look like in code for some file `my_job.py`:
```python
import sys
import random

def my_job(name):
    print(f"Hello {name}!")

    print("Random Number", random.randint(0, 100))

    print(f"Bye {name}!")


if __name__ == "__main__":
    arg = sys.argv[1]

    if not arg:
        raise Exception("You need to provide a name as input to continue!")
    my_job(arg)
```

Such a job would be run for example with:
```bash
python my_job.py "John"
```

### Part A: Defining the Job Configuration
Having a job that works, we can now move on to adding `trackerapi` on top of it to support tracking.

The first goal is to define the configuration for the job in a JSON file. This configuration will need to conform
to a specific format (a JSON Schema format).

1. First, generate the JSON Schema format files for the job configuration with:
    ```bash
    python -m trackerapi.generate_json_schemas
    ```
    > Tip: You can specify a location for the generated schemas with a `-l` flag. See "Scripts" section for more.

2. Once the schema has been generated, we can create our job configuration JSON file, with a `$schema`
field pointing to the location of the generated schemas from above. Create a new file `job_configurations.json` with the following
contents:

    ```json
    {
      "$schema": "./job-configurations-schema.generated.json",
      "job_configs": [
        {
          "name": "My Job",
          "tag": "my_job",
          "step_configurations": [
            {
              "name": "Say Hello",
              "tag": "say_hello",
              "points": 10
            },
            {
              "name": "Generate Random Number",
              "tag": "random_number",
              "points": 15
            },
            {
              "name": "Say Bye",
              "tag": "say_bye",
              "points": 10
            }
          ]
        }
      ]
    }
    ```

    > In this schema file, we define one job configuration, with a tag, "my_job", a display name, "My Job", and then a list
        of step_configurations, each with a unique tag, a display name, and points (indicating how much work is to be done for the step).

    > Tip: You can actually define multiple configurations in a single JSON file, and name the file whatever you want. Organization is up to you!

### Part B: Modifying Our Job with Tracking
Once we have the configuration above, we can now modify our job script to be able to start tracking progress
for users.

1. The first step in the process would be to load the configuration file into a `JobConfigManager` provided by `trackerapi`, and then
    fetch the specific configuration for `my_job`, using the tag `"my_job"` which we specified in `job_configurations.json`

    ```python
    import sys
    import random

    from trackerapi import JobConfigManager

    def my_job(name):
        # ADD THIS CODE
        job_config_manager = JobConfigManager(configurations_file="./job_configurations.json")
        job_config = job_config_manager.get_job_config("my_job")

        # ...


    if __name__ == "__main__":
        arg = sys.argv[1]

        if not arg:
            raise Exception("You need to provide a name as input to continue!")
        my_job(arg)
    ```

    > Note: The config manager extracts and validates the configuration file from the given JSON, and loads it into
        memory so that it can be accessed with a call to `manager.get_job_config(tag)` later.

2. Next, we can create a `TrackerApi` instance and specify your `api_key` and `base_url` to
the running backend service that you want to send jos to.

    ```python
    import sys
    import random

   # NEW IMPORT
    from trackerapi import JobConfigManager, TrackerApi

    def my_job(name):
        # ...

        # ADD THIS CODE
        tracker = TrackerApi(api_key="<your api key>", base_url="<url for tracker app backend>")

        # ...


    if __name__ == "__main__":
        arg = sys.argv[1]

        if not arg:
            raise Exception("You need to provide a name as input to continue!")
        my_job(arg)
    ```

3. Finally, we send calls to `tracker` to create a job, and then send events for that job. Each job requires a unique
`provider_job_id`.
    > NB: This `provider_job_id` can be used to query for information on the job at a later time.

    > NB: It also requires a `customer_id` which is one that is assigned to users that sign up for the application.

    ```python
    import sys
    import random
    import uuid

   # NEW IMPORT
    from trackerapi import JobConfigManager, TrackerApi

    def my_job(name):
        job_config_manager = JobConfigManager(configurations_file="./job_configurations.json")
        job_config = job_config_manager.get_job_config("my_job")

        tracker = TrackerApi(api_key="<your api key>", base_url="<url for tracker app backend>")

        # Create a unique ID for the job
        id = str(uuid.uuid4())
        tracker_job = tracker.create_job(provider_job_id=id, customer_id=142, tag=job_config.name)

        # Do the first step (The say_hello step)
        message = f"Hello {name}!"
        print(message)
        tracker_job.send_event(kind="step", name=job_config.step_configurations[0].tag, metadata={ "Message": message })

        # Do the second step (The random_number step)
        random_number = random.randint(0, 100)
        print("Random Number", random_number)
        tracker_job.send_event(kind="step", name=job_config.step_configurations[1].tag, metadata={ "Random Number": random_number })

        # Do the last step (The say_bye step)
        message = f"Bye {name}!"
        print(message)
        tracker_job.send_event(kind="step", name=job_config.step_configurations[2].tag, metadata={ "Message": message })


    if __name__ == "__main__":
        arg = sys.argv[1]

        if not arg:
            raise Exception("You need to provide a name as input to continue!")
        my_job(arg)
    ```

## Scripts

### `generate_json_schemas`
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
usage: generate_json_schemas.py [-h] [-l LOCATION] [-n NAME]

options:
  -h, --help            show this help message and exit
  -l LOCATION, --location LOCATION
                        Location of generated schemas
  -n NAME, --name NAME  Name to use for the generated <name>.generated.json schema file
```
