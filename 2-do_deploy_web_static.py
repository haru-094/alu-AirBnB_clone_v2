#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers."""
from fabric.api import env, put, run
import os

env.hosts = ['52.70.87.10', '3.93.218.74']
env.user = 'ubuntu'


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
