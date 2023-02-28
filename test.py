import PyXA
app = PyXA.Application("Bike")
doc = app.documents()[0]
row = doc.rows()[-1]
print(row.duplicate(row))









# import PyXA
# import AppKit
# import threading
# from time import sleep

# from PyObjCTools import AppHelper

# workspace = AppKit.NSWorkspace.sharedWorkspace()
# app = AppKit.NSApplication.sharedApplication()

# photos_app = PyXA.Application("Photos")
# photos = photos_app.media_items().equalling("isPhoto", True).shuffle()
# photo = PyXA.XAImage(photos[0])

# def random_photo_timer(app):
#     global photos, photo
#     while True:
#         sleep(5)
#         photos = photos.shuffle()
#         photo = PyXA.XAImage(photos[0])
#         app.setApplicationIconImage_(photo._nsimage)

# photo_thread = threading.Thread(target=random_photo_timer, args=(app, ))
# photo_thread.start()

# app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
# app.setApplicationIconImage_(photo._nsimage)

# AppHelper.installMachInterrupt()
# AppHelper.runEventLoop()