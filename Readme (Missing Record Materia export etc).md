Follow the install guide at https://redd.it/7xmdpw or the HTML file called "Install Guide.html"
Use the data exported with the FFRK Graphical Inventory Spreadsheet Mk3 at https://goo.gl/b2Zqb8

If you wish to remove shared Soul Breaks from the Soul Break export, edit line 144 to look for "categoryId >= 3" instead of 2. Alternatively if you want to export all your characters default soul break for some reason, change it to 1.

If you want to export your character info, uncomment the relevant code. Commented code begins with a "# " (That's a hash and a space), so delete that if you want to export.

Several other "useless" features have also been commented out. Feel free to uncomment them if you wish. 

Credits:
/u/vexnon for making the original mitmproxy scripts and a whole bunch of other tools.
/u/therealhughjeffner for a tip regarding the command line.
/u/Gitpush1337 for the expanded drop database csv file.
/u/csdx for making a Query() that made the filtered Enlir tabs usable.
The StackOverflow community for both being helpful angels and gatekeeping jackasses.