{
  description = "Febrace Analytics API";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;
      pkgsFor = nixpkgs.legacyPackages;
      name = "febraceapi";
      genSystems = lib.genAttrs [
        "aarch64-linux"
        "x86_64-linux"
      ];
    in
    rec {
      overlays.default = final: prev: rec {
        ${name} = final.callPackage ./default.nix { };
      };

      packages = genSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ overlays.default ];
          };
        in
        rec {
          febraceapi = pkgs.${name};
          default = febraceapi;
        });


      nixosModules.default = import ./module.nix;
    };
}
