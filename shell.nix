# Written by Vanu. Massive thanks to the entities on the forum;
# https://discourse.nixos.org/t/nix-shell-with-python-packages-through-pip/45825/4
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.pip
    python312Packages.virtualenvwrapper
    git
    curl
  ];

  shellHook = ''
    export TMPDIR=/tmp && export VENV=$(mktemp -d)
    virtualenv $VENV
    source $VENV/bin/activate
    pip install -r requirements.txt || exit
    circuitpython_setboard circuitplayground_express
  '';
}

