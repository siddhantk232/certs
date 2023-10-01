{
  description = "Python shell flake";

  inputs = { flake-utils.url = "github:numtide/flake-utils"; };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        django4 = with pkgs.python311Packages;
          buildPythonPackage rec {
            pname = "Django";
            version = "4.2.5";
            src = fetchPypi {
              inherit pname version;
              sha256 = "sha256-XlwclUj/t3lrSopHgumi5aPfNhUln8G/0+vHO2RhRsE=";
            };

            propagatedBuildInputs = [ asgiref sqlparse ];
            doCheck = false;
          };
        pythonEnv = pkgs.python311.withPackages
          (ps: with ps; [ openpyxl cairosvg django4 ]);
      in {
        devShells.default = pkgs.mkShellNoCC {
          packages = [ pythonEnv pkgs.pdftk pkgs.black pkgs.nixfmt ];

          shellHook = ''
            export PYTHONPATH="${pythonEnv}/bin/python"
          '';
        };
      });
}
