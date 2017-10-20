===============================================================================
ZenPacks.cascadeo.WorldAirQualityIndex
===============================================================================


About
===============================================================================

This ZenPack adds support for monitoring air quality using the 
World Air Quality Index API.


Features
-------------------------------------------------------------------------------

The following features are provided:

* air quality index (aqi) monitoring


Prerequisites
-------------------------------------------------------------------------------

==================  ========================================================
Prerequisite        Restriction
==================  ========================================================
Zenoss Platform     5.3
==================  ========================================================


Limitations
-------------------------------------------------------------------------------

Minimal error checking. Created as a sample only.


Usage
===============================================================================


Installation
-------------------------------------------------------------------------------

This ZenPack has no special installation considerations. You should install the
most recent version of the ZenPack for the version of Zenoss you're running.

To install the ZenPack you must copy the ``.egg`` file to your Zenoss master
server and run the following command as the ``zenoss`` user::

    zenpack --install <filename.egg>

After installing you must restart Zenoss by running the following command as
the ``zenoss`` user on your master Zenoss server::

    serviced service restart Zenoss.core

If installing via source, checkout from version control in directory shared 
among containers then install using::

    zenpack --link --install=ZenPacks.cascadeo.WorldAirQualityIndex


Configuring
-------------------------------------------------------------------------------

This ZenPack requires two configuration variables to be set:

* zWorldAirQualityIndexAPIKey: register through aqicn.org_ or waqi.info_ to get API
* zWorldAirQualityIndexLocations: copy name of station or location in waqi.info website.

.. _aqicn.org: http://aqicn.org
.. _waqi.info: http://waqi.info

Removal
-------------------------------------------------------------------------------

This ZenPack has no special removal considerations. To remove this ZenPack you
must run the following command as the ``zenoss`` user on your master Zenoss
server::

    zenpack --remove ZenPacks.cascadeo.WorldAirQualityIndex

You must then restart the master Zenoss server by running the following command
as user belonging to serviced group::

    serviced service restart Zenoss.core