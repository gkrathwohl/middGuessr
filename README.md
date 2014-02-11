middGuessr
==========

Makes a 'geoguessr'

Have a directory of images taken with location (iphone or something).

Edit geolocate.py so it knows where this directory is. If not .JPG images, edit that too.

Run geolocate.py, which generates imgs.js, which gives array of [img src, lat, lng].

Open main1.html in browser. It reads imgs.js, picks random images from array, displays them and lets you guess where they are on map.

Made for Middlebury, Vt. If somewhere else, change starting lat lng. 
