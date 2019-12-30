===========
AXL Defects
===========

Defects
=======

=================  ==================================================================================================
  Defect           Description
=================  ==================================================================================================
 **CSCvj27291**    AXL API for updateSyslogConfiguration - expecting correct value for "monitor"
 **CSCvj13556**    Invalid schema definition for GetRemoteDestinationReq in AXL 11.5
 **CSCvj13482**    getWLANProfile and addWLANProfile appear broken for EAP-TLS in 11.5
 **CSCvj13313**    11.5 RAudioCodecPreferenceList schema incorrectly defines maxOccurs="30"
 **CSCvj13354**    minOccurs settings for remoteDestinationProfileName and dualModeDeviceName in XRemoteDestination
=================  ==================================================================================================


Known Issues
============

The following are known AXL issues, but do not have official defects raised:

* XAddPhone violates nillability of confidentialAccessMode
* getLdapAuthentication is broken in 11.5
* XBusyLampField specifies minOccurs=1, which contradicts annotation, RBusyLampField behaviour
  and other AXL call choice options
* GetIlsConfigReq makes returnedTags mandatory - different from all other "get" requests
* 11.5 ListProcessNodeRes does not honour the schema sequence order for LProcessNode in actual response
