#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers."""
from fabric.api import env, local, put, run, settings
from datetime import datetime
import os

env.hosts = ['52.70.87.10', '3.93.218.74']
env.user = 'ubuntu'


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


def do_deploy(archive_path):
    """Distribute an archive to both web servers.

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if deployment succeeded on both servers, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    archive_file = os.path.basename(archive_path)
    archive_name = archive_file.replace('.tgz', '')
    release_path = '/data/web_static/releases/{}/'.format(archive_name)

    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_file, release_path))
        run('rm /tmp/{}'.format(archive_file))
        run('mv {}web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}web_static'.format(release_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))
        print('New version deployed!')
        return True
    except Exception:
        return False


def deploy():
    """Create and distribute an archive to both web servers.

    Returns:
        bool: True if deployment succeeded, False otherwise.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
