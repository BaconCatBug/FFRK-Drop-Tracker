Follow the install guide here: https://www.reddit.com/r/FFRecordKeeper/comments/6vhyod/ffrk_drop_tracker_export_your_entire_inventory/

If you wish to remove shared Soul Breaks from the Soul Break export, edit line 138 to look for "categoryId >= 3" instead of 2. Inversely if you want to export all your characters default soul break for some reason, change it to 1.

If you want to export your character info, uncomment the relevant code. Commented code begins with a #, so delete that if you want to export.