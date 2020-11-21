# -*- coding: utf-8 -

import pygame
import ktextsurfacewriter
from cheeseboys import cblocals

CHECK_NEW_VERSION_TEXT = (
    "Checking for a new version.\n"
    "Connecting to %s\n"
    "Please, wait..." % cblocals.URL_CHEESEBOYS_LAST_VERSION
)


def update_version(surface, rect):
    """Check for a new version of the game.
    Write output data on given surface and only inside the rect area.
    """
    import socket
    import urllib.request, urllib.parse, urllib.error
    import xml.dom.minidom

    timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(10)  # connection timeout
    ktswriter = ktextsurfacewriter.KTextSurfaceWriter(
        rect, font=cblocals.font_mini, color=(100, 255, 255, 0), justify_chars=3
    )
    ktswriter.text = CHECK_NEW_VERSION_TEXT
    try:
        ktswriter.draw(surface)
        pygame.display.flip()
        stream = urllib.request.urlopen(cblocals.URL_CHEESEBOYS_LAST_VERSION)
        dom = xml.dom.minidom.parse(stream)
        stream.close()
        root = dom.getElementsByTagName("cheeseboys-version")[0]
        date = root.getElementsByTagName("date")[0].firstChild.nodeValue
        version = root.getElementsByTagName("version")[0].firstChild.nodeValue
        version_type = root.getElementsByTagName("version")[0].attributes["type"].value
        changes = root.getElementsByTagName("changes")[0].firstChild.nodeValue.strip()
        if version != cblocals.__version__:
            ktswriter.text = "\n".join(
                [
                    "A new Cheese Boys version is available: %s (%s)."
                    % (version, version_type),
                    "Release date: %s\n" % date,
                    changes,
                    "\nPress any key to continue",
                ]
            )
        else:
            ktswriter.text = (
                CHECK_NEW_VERSION_TEXT + "\n\nYour Cheese Boys version is up to date."
            )
    except Exception as inst:
        print(inst)
        ktswriter.text = (
            CHECK_NEW_VERSION_TEXT
            + "\n\nAn error has been raised checking the new version. Please check you Internet connection."
        )
    finally:
        socket.setdefaulttimeout(timeout)  # restore base timeout
    still_inside = True
    while still_inside:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                still_inside = False
        ktswriter.draw(surface)
        pygame.display.flip()
