Japan:
Edit the variable at the top of FFRK_Inventory_Exporter_v3.xx.py to say "japan=1" instead of "japan=0".

This skips some Global only code.

Export Crappy Core Soul Breaks:
Edit the variable at the top of FFRK_Inventory_Exporter_v3.xx.py to say "ignore_crappy_core_soul_breaks=0".

Export Crappy Relics:
Edit the variable at the top of FFRK_Inventory_Exporter_v3.xx.py to say "ignore_three_star_and_lower_relics=0".

Soul Break Export Level:
Edit the variable at the top of FFRK_Inventory_Exporter_v3.xx.py to say:
"soul_break_export_level=1" to export ALL Soul Breaks, including Default Soul Breaks. 
"soul_break_export_level=2" to export Non-Default Soul Breaks, including Shared Soul Breaks.
"soul_break_export_level=3" to export Non-Default Soul Breaks, Non-Shared Soul Breaks.

Only export level 99 Magicite:
Edit the variable at the top of FFRK_Inventory_Exporter_v3.xx.py to say:
"only_export_level_99_magicite=1"

Raw json Export:
Edit the variable at the top of FFRK_Inventory_Exporter_v3.xx.py to say "export_raw_json=1"