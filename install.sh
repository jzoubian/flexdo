#!/usr/bin/env bash
# FlexDo Installation Script

set -e

echo "🚀 Installing FlexDo..."
echo ""

# Check if we're in a nix-shell or if nix is available
if command -v nix-shell &> /dev/null; then
    echo "✓ Nix detected. Building with nix-shell..."
    nix-shell --run "cargo build --release"
elif command -v cargo &> /dev/null; then
    echo "✓ Cargo detected. Building..."
    cargo build --release
else
    echo "❌ Error: Neither nix-shell nor cargo found."
    echo "Please install Rust or Nix to build FlexDo."
    exit 1
fi

echo ""
echo "✓ Build complete!"
echo ""
echo "To install flexdo system-wide, run:"
echo "  cargo install --path ."
echo ""
echo "Or run it directly from:"
echo "  ./target/release/flexdo"
echo ""
echo "📚 See USAGE.md for detailed usage instructions."
