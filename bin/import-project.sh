#!/bin/bash
# import-to-wsl.sh — Copie un dossier Windows vers WSL avec permissions propres

if [ $# -lt 1 ]; then
  echo "Usage: import-to-wsl <chemin_windows> [destination_wsl]"
  echo ""
  echo "Exemples:"
  echo "  import-to-wsl 'C:\\Users\\<user>\\Projects\\mon-projet'"
  echo "  import-to-wsl 'C:\\Users\\<user>\\Projects\\mon-projet' ~/projects/"
  exit 1
fi

WIN_PATH="$1"
DEST="${2:-$(pwd)}"

# Convertit le chemin Windows (C:\...) en chemin /mnt/c/...
WSL_PATH=$(echo "$WIN_PATH" | sed -e 's|\\|/|g' -e 's|^\([A-Za-z]\):|/mnt/\L\1|')

if [ ! -d "$WSL_PATH" ]; then
  echo "❌ Dossier introuvable : $WSL_PATH"
  echo "   (converti depuis : $WIN_PATH)"
  exit 1
fi

FOLDER_NAME=$(basename "$WSL_PATH")
TARGET="$DEST/$FOLDER_NAME"

echo "📂 Source  : $WSL_PATH"
echo "📁 Dest    : $TARGET"
echo ""

# Copie en excluant les dossiers qui doivent être régénérés
rsync -av --progress \
  --exclude 'node_modules' \
  --exclude 'vendor' \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '.pytest_cache' \
  --exclude '.mypy_cache' \
  --exclude 'dist' \
  --exclude 'build' \
  "$WSL_PATH/" "$TARGET/"

echo ""
echo "🔒 Correction des permissions..."

# Permissions saines : user rwx, group/other rx sur dossiers et fichiers exécutables
chmod -R u=rwX,go=rX "$TARGET"

# Protection stricte des fichiers sensibles
for sensitive in .env .env.local .env.production .env.development .env.staging; do
  if [ -f "$TARGET/$sensitive" ]; then
    chmod 600 "$TARGET/$sensitive"
    echo "   🔐 $sensitive → 600"
  fi
done

# Protection des clés SSH/certificats éventuels
find "$TARGET" -type f \( -name "*.pem" -o -name "*.key" -o -name "id_rsa*" -o -name "id_ed25519*" \) -exec chmod 600 {} \; 2>/dev/null

echo ""
echo "✅ Copié dans $TARGET"
echo ""
echo "📋 Prochaines étapes :"
echo "   cd $TARGET"
echo "   git status                 # vérifier l'état du repo"
echo "   # puis selon le projet :"
echo "   npm install                # Node.js"
echo "   pip install -r requirements.txt  # Python"
echo "   composer install           # PHP"
