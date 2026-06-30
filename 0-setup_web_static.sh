#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &>/dev/null; then
    apt-get update -y
    apt-get install -y nginx
fi

# Create required directory structure
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
cat > /data/web_static/releases/test/index.html << 'EOF'
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Delete existing symlink and recreate it every time
rm -f /data/web_static/current
ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ to ubuntu user and group, recursively
chown -R ubuntu:ubuntu /data/

# Add hbnb_static location to Nginx config if not already present
if ! grep -q "hbnb_static" /etc/nginx/sites-available/default; then
    sed -i "s|server_name _;|server_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}|" \
        /etc/nginx/sites-available/default
fi

# Restart Nginx
service nginx restart

exit 0
