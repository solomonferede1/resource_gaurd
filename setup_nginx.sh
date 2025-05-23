#!/bin/bash

# Install Nginx (with -y for automatic yes)
sudo apt-get update
sudo apt-get install -y nginx

# Create Nginx configuration file
sudo bash -c 'cat > /etc/nginx/sites-available/creativeaddis.tech <<EOF
server {
    listen 80;
    server_name www.creativeaddis.tech;

    # Serve the API
    location /api/ {
        include proxy_params;
        proxy_pass http://127.0.0.1:5000/;
    }

    # Serve the web app
    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:5050/;
    }

    # Serve static assets from your actual path
    location /static/ {
        alias /home/ubuntu/resource_gaurd/web_dynamics/static/;
        expires 30d;
    }
}
EOF'

# Enable the configuration
sudo ln -s /etc/nginx/sites-available/creativeaddis.tech /etc/nginx/sites-enabled/

# Set proper permissions for static files
sudo chown -R www-data:www-data /home/ubuntu/resource_gaurd/static
sudo chmod -R 755 /home/ubuntu/resource_gaurd/static

# Test configuration and restart Nginx
sudo nginx -t && sudo systemctl restart nginx

echo "Nginx configured with static files from /home/ubuntu/resource_gaurd/static"