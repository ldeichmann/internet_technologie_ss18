FROM python:3.6

ADD setup.py /pack/setup.py

ADD README.md /pack/README.md

ADD src /pack/src

RUN ls /pack

RUN cd /pack && pip install .

CMD [ "python3", "-m", "that_automation_tool.main", "-c", "/etc/tat_config.ini"]