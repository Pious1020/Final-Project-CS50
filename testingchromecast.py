import pychromecast


chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Master Chromecast TV"])

[cc.device.friendly_name for cc in chromecasts]