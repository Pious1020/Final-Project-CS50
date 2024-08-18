import pychromecast


chromecast, browser = pychromecast.get_listed_chromecasts(["Master Bedroom TV"])

cast = chromecast[0]

cast.wait()