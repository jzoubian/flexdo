{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Rust toolchain
    rustc
    cargo
    rustfmt
    clippy
    
    # Build dependencies
    gcc
    pkg-config
    
    # Audio libraries for rodio
    alsa-lib
    
    # Development tools
    git
  ];

  # Set environment variables
  RUST_BACKTRACE = "1";
  
  # Library path for dynamic linking
  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.alsa-lib
  ];

  shellHook = ''
    echo "FlexDo development environment"
    echo "Rust version: $(rustc --version)"
    echo "Cargo version: $(cargo --version)"
    echo ""
    echo "Available commands:"
    echo "  cargo build          - Build the project"
    echo "  cargo run -- [args]  - Run the application"
    echo "  cargo test           - Run tests"
    echo ""
  '';
}
