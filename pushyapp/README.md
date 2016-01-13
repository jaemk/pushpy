# Pushy.py

Listen to pushbullet feed for commands. Send picture to main user when requested ('send cat', 'send dog').

Requires:

* "pushbullet.py" library: (https://github.com/randomchars/pushbullet.py) `pip install pushbullet.py`
* An opencv install: (a test pic will be sent if opencv isn't installed)
  * compile from source... see [pyimagesearch](http://www.pyimagesearch.com/2015/07/27/installing-opencv-3-0-for-both-python-2-7-and-python-3-on-your-raspberry-pi-2/)
  * or do a dirty and install using apt-get `apt-get install python-opencv` (only python2 bindings) 
* Rename `settings_copy.py` to `settings.py` -- enter personal pushbullet api key and main user's name


Ownership of "cam.py" may need to be changed to root for hw acces. See "settings.py" for setup information.

