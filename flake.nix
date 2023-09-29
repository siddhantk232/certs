{
  description = "Python shell flake";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = pkgs.python3.withPackages(ps: with ps; [ openpyxl cairosvg ]);
      in
      {
        devShells.default = pkgs.mkShellNoCC {
          packages = [ pythonEnv ];

          shellHook = ''
            export PYTHONPATH="${pythonEnv}/bin/python"
          '';
        };
      }
    );
}
