
=================================================================================================

This directory contains technical notes that apply to a new implementation of Ricoh Gen4 heads only.
Following head types supported:


    head type:      Head type name          Default config files:
                    in the config file:

    HT_RicohGen4    "Ricoh_Gen4"            Default_Ricoh_Gen4_PccE.cfg           
    HT_RicohGen4L   "Ricoh_Gen4L"           Default_Ricoh_Gen4L_PccE.cfg
  
=================================================================================================

So, these new head types present better implementation for Ricoh Gen4/Gen4L heads driven by HDC-R4.
These heads supported only on a PCC-E.

"Gen4L" (HT_RicohGen4L) head type is, basically, the same as GEN4, apart from nozzle row separation (0.9948mm) 
and 150 DPI resolution. It has turned out to be easier to introduce a new head type to address such differences. 
All other parameters and settings are absolutely the same as for HT_RicohGen4 type.


  