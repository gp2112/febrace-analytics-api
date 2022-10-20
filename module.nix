{ config, lib, pkgs, ... }:

with lib;
let
  cfg = config.services.febraceapi;
  settingsFormat = pkgs.formats.toml {};
in {

  options.services.querolerbot = {
    enable = mkEnableOption "febraceapi service";

    package = mkOption {
      type = types.package;
      default = pkgs.febraceapi;
    };

    user = mkOption {
      type = types.str;
      default = "febraceapi";
    };

    credentialsFile = mkOption {
      type = types.str;
      default = "~/.aws/credentials";
    };

    port = mkOption {
      type = types.int;
      default = 5000;
    };

  };

  config = mkIf cfg.enable {
    services.febraceapi.settings = {
      general.delay = mkDefault 15;

    };


    users.users.${cfg.user} = {
      home = "/var/${cfg.user}/";
      isSystemUser = true;
      group = cfg.user;
      createHome = true;
    };

    users.groups.${cfg.user} = {};

    systemd.services.febraceapi = {
      description = "Febrace Middleware API";
      wantedBy = [ "multi-user.target" ];
      environment = {
        AWS_CREDENTIALS_PATH = cfg.credentialsFile;
        FEBRACEAPI_PORT = cfg.port;
      };
      serviceConfig = {
        ExecStart = "${cfg.package}/bin/febraceapi";
        Restart = "on-failure";
        User = cfg.user;
      };
      reloadIfChanged = true;
    };
  };
}
