FROM nginx:stable

COPY sites/mock-ckan.conf /etc/nginx/conf.d/mock-ckan.conf
COPY vars.conf /etc/nginx/vars.conf
COPY responses/ /srv/responses
COPY mock-third-party/ /srv/mock-third-party

RUN rm -f /etc/nginx/conf.d/default.conf && \
  sed -E -i 's|^http \{|\0 map $host $mock_ckan_responses_root { default /srv/responses; } map $host $mock_third_party_root { default /srv/mock-third-party; } include /etc/nginx/vars.conf;|' /etc/nginx/nginx.conf && \
  sed -E -i 's|\b11088\b|80|' /etc/nginx/conf.d/mock-ckan.conf
