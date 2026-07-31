#!/bin/bash
# deploy.sh — Sube el cancionero a GitHub Pages
# Requiere: config.env con GITHUB_TOKEN, GITHUB_USER, GITHUB_REPO

set -e

# Buscar config.env en el mismo directorio que este script o en el padre
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG="${SCRIPT_DIR}/config.env"
[ ! -f "$CONFIG" ] && CONFIG="${SCRIPT_DIR}/../config.env"

if [ ! -f "$CONFIG" ]; then
  echo "❌ No se encontró config.env"
  echo "   Creá el archivo con:"
  echo "   GITHUB_TOKEN=ghp_tutoken"
  echo "   GITHUB_USER=tu-usuario"
  echo "   GITHUB_REPO=cancionero-pjsi"
  exit 1
fi

source "$CONFIG"

if [ -z "$GITHUB_TOKEN" ] || [ -z "$GITHUB_USER" ] || [ -z "$GITHUB_REPO" ]; then
  echo "❌ Faltan variables en config.env"
  exit 1
fi

COMMIT_MSG="${1:-Actualizar cancionero}"
REPO_DIR="/tmp/cancionero_deploy_$$"
SRC="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "📦 Clonando repo..."
git clone --quiet --depth 1 "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git" "$REPO_DIR"

echo "📋 Copiando archivos..."
cp "$SRC/index.html"    "$REPO_DIR/"
cp "$SRC/style.css"     "$REPO_DIR/"
cp "$SRC/app.js"        "$REPO_DIR/"
cp "$SRC/songs_data.js" "$REPO_DIR/"
cp "$SRC/general_songs_data.js" "$REPO_DIR/"
cp "$SRC/README.md"     "$REPO_DIR/"
mkdir -p "$REPO_DIR/scripts"
cp "$SRC/scripts/"*.py "$REPO_DIR/scripts/" 2>/dev/null || true
cp "$SRC/scripts/config.env.example" "$REPO_DIR/scripts/" 2>/dev/null || true

cd "$REPO_DIR"
git config user.email "bot@cancionero.local"
git config user.name "Cancionero Bot"

git add -A

if git diff --cached --quiet; then
  echo "✓ Sin cambios, nada que deployar."
  rm -rf "$REPO_DIR"
  exit 0
fi

git commit -m "$COMMIT_MSG"
echo "🚀 Pusheando..."
git push --quiet

rm -rf "$REPO_DIR"
echo ""
echo "✅ Deploy exitoso!"
echo "🌐 https://${GITHUB_USER}.github.io/${GITHUB_REPO}"
