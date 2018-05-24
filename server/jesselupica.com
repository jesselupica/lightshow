##
# You should look at the following URL's in order to grasp a solid understanding
# of Nginx configuration files in order to fully unleash the power of Nginx.
# http://wiki.nginx.org/Pitfalls
# http://wiki.nginx.org/QuickStart
# http://wiki.nginx.org/Configuration
#
# Generally, you will want to move this file somewhere, and start with a clean
# file but keep this around for reference. Or just disable in sites-enabled.
#
# Please see /usr/share/doc/nginx-doc/examples/ for more detailed examples.
##

# Default server configuration
#
server {	      

	root /var/www/jesselupica.com/html;

	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;

	      server_name jesselupica.com www.jesselupica.com;
	
	location / {
	      proxy_set_header X-Real-IP $remote_addr;
	      proxy_set_header Host $host;
	     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	     proxy_pass http://0.0.0.0:8000;
	     # proxy_set_header   Host $host;
	     # proxy_set_header   X-Real-IP $remote_addr;
	     # proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
	     #             proxy_set_header   X-Forwarded-Host $server_name;
	     
	       }

	# pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
	#
	#location ~ \.php$ {
	#	include snippets/fastcgi-php.conf;
	#
	#	# With php7.0-cgi alone:
	#	fastcgi_pass 127.0.0.1:9000;
	#	# With php7.0-fpm:
	#	fastcgi_pass unix:/run/php/php7.0-fpm.sock;
	#}

    listen [::]:443 ssl ipv6only=on; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/jesselupica.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/jesselupica.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}

server {
    if ($host = www.jesselupica.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = jesselupica.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


	listen 80 default_server;
	listen [::]:80 default_server;

	      server_name jesselupica.com www.jesselupica.com;
    return 404; # managed by Certbot




}
