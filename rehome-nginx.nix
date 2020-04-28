{ stdenv
, symlinkJoin
, writeText
, makeWrapper
, nginx
, sitesDir
, logDir
, runDir
, responsesDir
, thirdPartyDir
, varsConf
}:

symlinkJoin {
  name = "rehomed-nginx";
  paths = [ nginx ];
  nativeBuildInputs = [ makeWrapper ];
  # this nginx.conf indended to have minimal variation from nginx docker image's default
  nginxConf = writeText "nginx.conf" ''
    worker_processes  1;

    error_log  ${logDir}/error.log info;
    pid        ${runDir}/nginx.pid;

    events {
        worker_connections  1024;
    }

    http {
        # abusing `map` here because `set` is not allowed in this context
        map $host $mock_ckan_responses_root { default ${responsesDir}; }
        map $host $mock_third_party_root { default ${thirdPartyDir}; }
        include ${varsConf};

        include       mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for" "$realpath_root" "$request_uri" "$uri"';

        access_log  ${logDir}/access.log  main;
        client_body_temp_path ${runDir}/cbtmp;
        proxy_temp_path ${runDir}/ptmp;
        fastcgi_temp_path ${runDir}/ftmp;
        uwsgi_temp_path ${runDir}/utmp;
        scgi_temp_path ${runDir}/stmp;

        sendfile        on;
        #tcp_nopush     on;

        keepalive_timeout  65;

        #gzip  on;

        include ${sitesDir}/*.conf;
    }
  '';
  postBuild = ''
    rm $out/conf/nginx.conf
    ln -s $nginxConf $out/conf/nginx.conf
    wrapProgram $out/bin/nginx \
      --run "mkdir -p ${sitesDir} ${logDir} ${runDir} ${thirdPartyDir} ${responsesDir}" \
      --add-flags "-c $out/conf/nginx.conf"
  '';
}
