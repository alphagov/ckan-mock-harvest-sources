# CKAN (static) mock harvest-source

This repo contains configuration for nginx to be able to easily serve static
responses to arbitrary GET requests based on path *and* query-string. These can
be placed under `responses/json/` and will be served to the requester with the
`application/json` mimetype. If a file matching the request path+querystring can't
be found, nginx will look for a matching file in `responses/html/` and serve it with
a `text/html` mimetype, failing that it will serve files under `responses/xml/` as
`text/xml`. These are intended to allow mocking of the responses to CKAN's harvesting
mechanism, and example finctionalized data is provided for this purpose.

Files under `responses/` are all processed by nginx's SSI module to allow some basic
substitutions to take place in the returned data. A `vars.conf` file allows site-specific
variables to be set - at this point it's just for setting `$mock_absolute_root_url`
to the  externally-visible url this server is accessible through. Together these
allow cross-endpoint references to work.

There is also a directory `mock-third-party/` whose contents will be served fairly
normally, assigning a mimetype using nginx's regular filename-extension-based
mechanism. This is intended to be used to serve actual files that can be referenced
in a package's `resources`.

The server can be run in two ways:

 - For easy development a user with a working Nix installation should just be able
   to run `nix-shell . --pure --run "nginx"` to start an nginx daemon running
   locally.
 - A `Dockerfile` is also provided for more permanent deployments.
