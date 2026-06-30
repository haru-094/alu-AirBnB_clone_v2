#!/usr/bin/python3
"""Fabric script that creates a .tgz archive from the web_static."""
from fabric.api import local, settings
from datetime import datetime
import os


def do_pack():
    """Create a .tgz archive from the contents of the web_static folder.

    Returns:
        str: The archive path if successfully created, None otherwise.
    """
    local("mkdir -p versions")
    now = datetime.now()
    archive_name = "web_static_{}{:02d}{:02d}{:02d}{:02d}{:02d}.tgz".format(
        now.year, now.month, now.day,
        now.hour, now.minute, now.second
    )
    archive_path = "versions/{}".format(archive_name)
    print("Packing web_static to {}".format(archive_path))
    with settings(warn_only=True):
        result = local("tar -cvzf {} web_static".format(archive_path))
    if result.failed:
        return None
    size = os.path.getsize(archive_path)
    print("web_static packed: {} -> {}Bytes".format(archive_path, size))
    return archive_path
