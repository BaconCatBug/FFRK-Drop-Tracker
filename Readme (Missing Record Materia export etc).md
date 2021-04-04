Follow the install guide at https://redd.it/atobpm or the HTML file called "Install Guide.html"
Use the data exported with the FFRK Graphical Inventory Spreadsheet at https://docs.google.com/spreadsheets/d/1aJ-y4b2-ulyEJHO2-FuH8mQkmaSrPKN04bwWHOWIFWI
or with FFRK Inventory Stats and Dud Relic Finder https://docs.google.com/spreadsheets/d/1DblycHYZQySX00fVgrnj8IUltd6-rld3XqSR9tpTG7A

If you want to export your character info, uncomment the relevant code. Commented code begins with a #, so delete that if you want to export.

Several other "useless" features have also been commented out. Feel free to uncomment them if you wish. 

Credits:
/u/vexnon for making the original mitmproxy scripts and a whole bunch of other tools.
/u/therealhughjeffner for a tip regarding the command line.
/u/Gitpush1337 for the expanded drop database csv file.
/u/csdx for making a Query() that made the filtered Enlir tabs usable.
The StackOverflow community for both being helpful angels and gatekeeping jackasses.

Changelog

#Updated to 6.18

##FFRK Relic Inventory Stats and Dud Relic Finder v6.18

* The Dud Relic finder now has an additional parameter for an alternate "Filter Top" value for Mnd relics. Combine it with the "Yes (Except for Mnd Gear)" option to more aggressively prune no elemental boost Mind Statsticks.

## FFRK Relic Inventory Stats and Dud Relic Finder v6.18

* Sync Command now have a dedicated page the same as BSB commands do!
* I fixed the sorting options on some of the pages were it was broken.
* Fixed the Orb screen to now be in the correct order and made the background match the rest of the sheet!
* Fixed the Legend Materia page to use the Community Database data rather than the in-game descriptions.
* Tweaked some of the back end scripts for pulling and processing the data from the Community Database, so now it shouldn't ever break even if they add or remove extra columns.  
* Also tweaked the scripts to remove as much redundant data from the database importing, hopefully improving performance when you're updating the database.
* Renamed mentions of Enlir's Database to Community Database. It's tearing me apart, ~~Lisa!~~ but it's time to move on.
* Did some tweaking of vLookups across the sheet to try and remove redundant data from them to help performance.
* Set the Database and Calc sheets as hidden by default. They are still there obviously, just not cluttering the bottom bar.
* Oh and added a changelog to the github since I never thought of doing that before.

## The beacon is lit, Gondor calls for aid!

So, I don't know if it's sleep deprivation or just plain old senility, but I've been trying to get a working setup for a Status effects page and I can't get it working for love nor money. It might simply be a limitation of Google Sheets, but I'll put it out there just in case someone is amazing and is like "Why are you do dumb, just do this." Basically I need some way of extracting all the bracketed statuses from the list of Soul Breaks the user of the spreadsheet has, and turning them into a list. My Regex-fu failed me and I only got as far as a partial (but not always) successful extraction of the statuses but then failed to combine them into a usable column for cross-referencing. If anyone has any ideas, please let me know I'd love to get that working.


# Updated to 6.17
## FFRK Relic Inventory Stats and Dud Relic Finder v6.17								
* Fixed the conditional formatting for the Inventory Stats Atk column
* Fixed an issue with Rosetta Stone augment points not having synergy applied to them.
* Refactored the back-end calculation of the best-in-slot gear. 
 * There is now less redundant data for the main query to wade though.
 * Tied relics edge case should no longer happen now (you'd need over 500 relics total for a single realm taking up the top slots for an error to happen, and if you somehow manage to do this unintentionally I will be thoroughly impressed).

## FFRK Relic Inventory Stats and Dud Relic Finder v6.17	
* Added automatic escaping of special characters (+-[]%) in the effects search to account for the fact Regex uses those characters for special purposes.
* Added explicit note about the need to still manually escape searching for terms starting with + or - (as Google Sheets considers cells starting with + or - to be formulas). e.g. If you want to search for `+30% MAG` it needs to formatted as `'+30% MAG`

#Updated to 6.16
* Added the option to ignore "best in slot" non-elemental equipment (aka Stat Sticks) as equipment without elemental boosts is pretty useless
* Also added the option to ignore "best in slot" non-elemental equipment (aka Stat Sticks) except for Mnd Statsticks as healers generally don't need the elemental boost.
* Let me know if anything seems off, it looks ok to me.

#Updated to 6.15
* Fixed a stupid regression regarding Limit Breaks, again. Sorry!

#Updated to 6.14
* Fixed an issue related to Limit Breaks not displaying correctly.
* Fixed an issue related to the import of Limit Break data.
* Updated the terminology for ADSB.

#Updated to 6.13
* Fixed an issue with the Database update scripts, caused by a Google bug with the UrlFetchApp.fetch() function. They should work again now.

#Updated to 6.12

* Added support for Limit Break Glints and Limit Break Overflows.
* Fixed an issue with the Database update scripts.
* Fixed an issue with Sorting incorrectly Sorting Sometimes.

#The scripts can be found here, just click Code > Download Zip: https://github.com/BaconCatBug/FFRK-Drop-Tracker

Due to the length of the installation guide (as I now wrote up how to do it for Bluestacks too), the guide has been permanently moved to the HTML file found on Github. This thread remains to post enquiries and support questions.

Changes before 6.12 are lost to the æther.