from urllib.request import HTTPError #py3
import tkinter as tk
#from urllib2 import HTTPError #py2
#... 
def load_image_to_base64(image_url):
    """ Load an image from a web url and return its data base64 encoded"""
    image_byt = urlopen(image_url).read()
    image_b64 = base64.encodestring(image_byt)
    return image_b64

# load photos to photos list
urllist = ['http://www.okclipart.com/img16/kjlhjznjvkokwqpalupl.png', 
           'invalidurltest', 
           'http://www.okclipart.com/YouWontFindThisImage.png']
photos = []
for i, url in enumerate(urllist):
    print(i,"loading",url)
    try:
        photo = tk.PhotoImage(data=load_image_to_base64(url))
        photos.append(photo)
        print("done")
    except HTTPError as err:
        print("image not found, http error code:", err.code)
    except ValueError:
        print("invalid url", url)

# iterate through photos and put them onto the canvas
for photo in photos:
    cv.create_image(10*i, 10*i, image=photo, anchor='nw')

root.mainloop()