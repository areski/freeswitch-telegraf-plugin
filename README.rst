
Telegraf plugin for FreeSWITCH
==============================

FreeSWITCH-Telegraf-Metrics is a Python application that collect the following FreeSWITCH metrics:

    - Total of active channels
    - Total of calls
    - Current CPS

This plugin uses Telegraf exec input plugin to execute abritary commands, see https://github.com/influxdata/telegraf/tree/master/plugins/inputs/exec


Usage
-----

Usage example::

    export FS_HOST="localhost"; export FS_PORT=8080; export FS_USERNAME="freeswitch"; export FS_PASSWORD="works"
    ./freeswitch_metrics.py


Installation
------------

There is no PIP package for this plugins, please open a PR/Issue if you feel the need for one.

You can install the telegraf plugin script as follow:

    mkdir /opt/freeswitch-telegraf-plugin/
    cd /opt/freeswitch-telegraf-plugin/
    wget https://raw.githubusercontent.com/areski/freeswitch-telegraf-plugin/master/freeswitch_metrics.py


Configuration
-------------

After installing Telegraf, you will need to use the inputs exec plugin [https://github.com/influxdata/telegraf/tree/master/plugins/inputs/exec]

Add in your /etc/telegraf/telegraf.conf file the following config::

    # Read flattened metrics from one or more commands that output JSON to stdout
    [[inputs.exec]]
      # the command to run
      command = "/opt/freeswitch-telegraf-plugin/freeswitch_metrics.py"

      # Data format to consume. This can be "json" or "influx" (line-protocol)
      # NOTE json only reads numerical measurements, strings and booleans are ignored.
      data_format = "json"

      # measurement name suffix (for separating different commands)
      name_suffix = "_freeswitch"


You will need to edit the following settings in freeswitch_metrics.py to match your XML RPC FreeSWITCH configuration:

    - FS_HOST - default: localhost
    - FS_PORT - default: 8080
    - FS_USERNAME - default: freeswitch
    - FS_PASSWORD - default: works

Don't forget to enable FreeSWITCH XML RPC module (https://freeswitch.org/confluence/display/FREESWITCH/mod_xml_rpc)!


Collected Metrics
-----------------

You will now have 3 metrics collected and pushed by Grafana:

    - active_channels
    - active_calls
    - cps


License
-------

FreeSWITCH-Telegraf-Metrics is licensed under MIT, see `LICENSE` file.


TODO
----

    * Add Telegraf support for ENV variables
