# that automation tool

This tool was developed during the summer of 2018 for the internet technology
project course at the University Lübeck. It is currently undergoing development
and focused on passing the required milestones until we're allowed to implement
our own ideas.

The library is targeting Raspberry Pis running Raspbian Strech using Python 3.5,
it is likely able to run on other systems.

## Getting started

### Installation
The library is provided as a Python package, meaning it may be installed using pip.
A Dockerfile is provided for testing purposes.

### Configuration
A sample configuration is provided in sample_config.ini

### Running
After a successful installation the library may be run using `python3 -m that_automation_tool.main -c /path/to/config`.

### Running docker image
After building the image, the container may be run with
`docker run --volume="/path/to/your/config.ini:/etc/tat_config.ini" --volume="</serial/device>:</config/path/to/serial/device?" --privileged <image id>`
#### Explanations
1. The Dockerfile expects the configuration to be at /etc/tat_config.ini,
so we're mounting it as a volume there
2. The real serial port is mapped to the path you've specified in your configuration.
If you're not using LDR in your Configuration, it may be left out.
3. `--privileged` is necessary to access the Raspberry Pis GPIO Pins
4. `<image id>` is the ID the image received when you built it