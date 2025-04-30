{
  description = "Flake packaging for lexisort script across multiple platforms";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      allSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      forAllSystems = f: nixpkgs.lib.genAttrs allSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      packages = forAllSystems ({ pkgs }:
        let
          lexisortScript = pkgs.stdenv.mkDerivation {
            pname = "lexisort";
            version = "0.1"; # Use your script's version
            src = ./.; # Point to your source directory

            # Define the build steps (phases)
            # We only need the installPhase to copy the script
            installPhase = ''
              mkdir -p $out/bin
              # Copy your script and make it executable
              # Assuming your script is named lexisort.py
              cp lexisort.py $out/bin/lexisort
              chmod +x $out/bin/lexisort
              # If your script needs a shebang (e.g., #!/usr/bin/env python3)
              # make sure it's present and correct, or wrap it:
              # pkgs.makeWrapperArgs --wrap $out/bin/lexisort --prefix PATH : ${pkgs.python3}/bin
              '';

            # Add buildInputs if your script depends on other packages at build time (unlikely for a simple script)
            buildInputs = [];

            # Add runtime dependencies if your script needs other packages to run
            # It will need Python to run
            nativeBuildInputs = [ pkgs.python3 ]; # Need python3 available during build for the script
            # Or add python3 to runtime dependencies if you use makeWrapper
            # runtimeDependencies = [ pkgs.python3 ];
          };
        in
        {
          lexisort = lexisortScript;
          default = lexisortScript; # Make it the default package
        }
      );
    };
}
