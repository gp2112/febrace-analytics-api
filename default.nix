{ lib, python310Packages, pkgs, ... }:

let
  vnumber = "1.0.0";
in
python310Packages.buildPythonApplication rec {

  pname = "febraceapi";
  version = "${vnumber}";

  src = ./.;

  format = "pyproject";

  propagatedBuildInputs = with pkgs.python310Packages; [
    boto3
    fastapi
    uvicorn
    setuptools
    toml
  ];

  meta = with lib; {
    description = "API Middleware para plataforma Febrace Analytics";
    homepage = "https://github.com/gp2112/febrace-analytics-api";
    platforms = platforms.all;
  };

}
