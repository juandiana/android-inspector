Android Inspector
=================

Overview
--------
*Android Inspector* is a forensic command-line tool that lets you extract & examine data from Android mobile devices.
You may choose to extract data of different types and from sources by using the different operations it brings.
The information examined is then represented using the `CybOX language`_.

This tool is part of the undergraduate thesis *Data extraction from mobile devices* by Juan Andrés Diana and José
Ignacio Varela.

Example
-------
.. code-block:: bash

    ￼$ ./andi.py
    Android Inspector v1.0

    (Andi) set_device_info −m XT1053 −v 4.3
    Device model ’XT1053’ running Android version ’4.3’ was set as the current device information.

    (Andi) list
    Name                   Data type     Data Source                                                Devices supported           Android versions supported
    ---------------------  ------------  ---------------------------------------------------------  --------------------------  ----------------------------
    EmailMessageAOSPEmail  EmailMessage  Application{package_name:com.android.email}                [GT-I9300, XT1053]          [2.3.7-5.1.1]
    SmsMessageAOSPSms      SMSMessage    Application{package_name:com.android.providers.telephony}  [GT-I9300, XT1053]          [2.2.0-4.4.4]
    ContactFacebook        Contact       Application{package_name:com.facebook.katana}              [GT-I9300, Nexus5, XT1053]  [4.1-4.4.4]
    ContactWhatsApp        Contact       Application{package_name:com.whatsapp}                     [GT-I9300, XT1053]          [4.1-4.4.4]
    ContactAOSPAgenda      Contact       Application{package_name:com.android.providers.contacts}   [GT-I9300, XT1053]          [2.3-4.4.4]


    (Andi) execute −op SmsMessageAOSPSms
    [1/1] Executing ’SmsMessageAOSPSms’:
    Fetching ’/system/app/TelephonyProvider.apk’ file ...
    Fetching ’/data/data/com.android.providers.telephony’ directory ...
    COMPLETED. Data stored to ’results/SmsMessageAOSPSms_20150826_081415’. 1 operation(s) completed successfully.

Requirements
------------
- Python 2.7
- *Java 6 (Optional: Used for HTML output generation only)*

**Python dependencies:**

- python-cybox (2.1.0.12)
- python-magic (0.4.6)
- python-tabulate (0.7.5)
- *nose-parameterized (0.5.0) (Optional: Used to run the tests only)*

**Other dependencies:**

- adb (from the Android SDK Platform Tools)
- aapt (from the Android SDK Build Tools)

Installation
------------
1. Download this repository and extract it to a directory on your system.

2. To install the Python dependencies automatically run:

.. code-block:: bash

    $ pip install −r requirements.txt

3. Add the platform-tools & build-tools directories of the Android SDK to your PATH environment variable.

.. code-block:: bash

    $ export ANDROID_HOME=/Path/to/Android/sdk
    $ export PATH=$PATH:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/22.0.1

4. If you wish to make use of the HTML generation, add your Java directory to your PATH also.

.. code-block:: bash

    $ export PATH=$PATH:$JAVA_HOME/bin/

5. Make the Python scripts executable by running:

.. code-block:: bash

    $ chmod +x andi.py load_data_sets.py

Usage
-----
You may start by loading into your test device a test dataset from the ``datasets/`` directory as follows:

.. code-block:: bash

    $ ./load_data_sets.py HTC_Evo_3D

Then, just initiate *Android Inspector* in interactive mode, like so:

.. code-block:: bash

    $ ./andi.py
    Android Inspector v1.0

You may then use the following commands to operate:

=============== ========================================================================================================
Command         Description
=============== ========================================================================================================
set_device_info Sets the device information (i.e. device model and Android version).
list            Lists all the available operations for the device set and lets you filter by data type and data source.
execute         Executes a list of operations.
=============== ========================================================================================================

Extending the tool
------------------
If you wish to extend the tool's functionality you may develop DataType, DataSourceType or Operation extensions and
users of the tool may import it using the `add_ext` and `rm_ext`. E.g.:

.. code-block:: bash

    $ ./andi.py add_ext data_type path/to/new_data_type_definition.tar

    $ ./andi.py rm_ext data_type new_data_type_name

Layout
------
The tool's structure is:

============ ==================================================================
Package      Description
============ ==================================================================
components   Core components of the tool.
model        Data model classes.
repositories Extensions (DataTypes, DataSourceTypes & Operations) repositories.
test         UnitTests & testing resources.
util         Utility modules for developing extensions.
============ ==================================================================

Documentation
-------------
The code reference documentation may be built using *Sphenix* as follows:

.. code-block:: bash

    $ sphinx-build -b html docs/source/ docs/build/

To access the generated docs, go to ``/docs/build/index.html``.

Notice
------
This tool also makes use of `device.py`_ (from the Android Open Source Project) and `STIX-to-HTML`_ (from the STIX Project).

Authors
-------
| Juan Andrés Diana
| José Ignacio Varela
|
| Grupo de Seguridad Informática
| Facultad de Ingeniería
| Universidad de la República


.. _CybOX language: https://cybox.mitre.org/
.. _device.py: https://android.googlesource.com/platform/system/core/+/master/adb/device.py
.. _STIX-to-HTML: https://github.com/STIXProject/stix-to-html