argsOuter@{...}:
let
  # specifying args defaults in this slightly non-standard way to allow us to include the default values in `args`
  args = rec {
    pkgs = import <nixpkgs> {};
    localOverridesPath = ./local.nix;
  } // argsOuter;
  rehomeNginx = import ./rehome-nginx.nix;
in (with args; {
  ckanMockHarvestSourceEnv = (pkgs.stdenv.mkDerivation rec {
      name = "ckan-mock-harvest-source-env";
      shortName = "ck-mk-hvst-src";
      buildInputs = [
        (rehomeNginx {
          inherit (pkgs) stdenv writeText symlinkJoin makeWrapper;
          nginx = pkgs.nginx;
          sitesDir = (toString (./.)) + "/sites";
          logDir = (toString (./.)) + "/nix-var/logs";
          runDir = (toString (./.)) + "/nix-var/run";
          responsesDir = (toString (./.)) + "/responses";
          thirdPartyDir = (toString (./.)) + "/mock-third-party";
          varsConf = (toString (./.)) + "/vars.conf";
        })
        pkgs.cloudfoundry-cli
      ];

      # if we don't have this, we get unicode troubles in a --pure nix-shell
      LANG="en_GB.UTF-8";

      shellHook = ''
        export PS1="\[\e[0;36m\](nix-shell\[\e[0m\]:\[\e[0;36m\]${shortName})\[\e[0;32m\]\u@\h\[\e[0m\]:\[\e[0m\]\[\e[0;36m\]\w\[\e[0m\]\$ "
      '';
    }
  ).overrideAttrs (if builtins.pathExists localOverridesPath then (import localOverridesPath args) else (x: x));
})
