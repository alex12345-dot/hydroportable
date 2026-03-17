#!/usr/bin/env bash
# =============================================================================
# build_apk.sh – Build and sign the Moto Uniforme APK for Play Store
# =============================================================================
set -e

echo "=== Moto Uniforme – Build APK per Play Store ==="

# 1. Sync HTML into Android assets (in case index.html was edited)
echo "[1/5] Copia index.html negli assets Android..."
cp index.html android/app/src/main/assets/index.html

# 2. Download Gradle wrapper if needed
echo "[2/5] Verifica Gradle wrapper..."
cd android
if [ ! -f gradlew ]; then
    echo "Scaricamento Gradle wrapper..."
    curl -sL "https://services.gradle.org/distributions/gradle-8.6-bin.zip" -o /tmp/gradle.zip
    unzip -q /tmp/gradle.zip -d /tmp/gradle-dist
    /tmp/gradle-dist/gradle-8.6/bin/gradle wrapper --gradle-version=8.6
fi

# 3. Build release APK
echo "[3/5] Build release APK..."
./gradlew assembleRelease

# 4. Sign the APK with your keystore
# USAGE: Set these environment variables before running this script:
#   KEYSTORE_PATH   – path to your .jks / .keystore file
#   KEY_ALIAS       – key alias
#   KEYSTORE_PASS   – keystore password
#   KEY_PASS        – key password
echo "[4/5] Firma APK..."
UNSIGNED_APK="app/build/outputs/apk/release/app-release-unsigned.apk"
SIGNED_APK="../moto-uniforme-release.apk"

if [ -z "$KEYSTORE_PATH" ]; then
    echo "ATTENZIONE: variabile KEYSTORE_PATH non impostata."
    echo "Per firmare l'APK, esegui:"
    echo "  export KEYSTORE_PATH=/path/to/keystore.jks"
    echo "  export KEY_ALIAS=my_key"
    echo "  export KEYSTORE_PASS=password"
    echo "  export KEY_PASS=password"
    echo "  bash build_apk.sh"
    echo ""
    echo "Per creare un nuovo keystore:"
    echo "  keytool -genkey -v -keystore keystore.jks -alias moto_uniforme -keyalg RSA -keysize 2048 -validity 10000"
    cp "$UNSIGNED_APK" "$SIGNED_APK"
    echo "APK non firmato copiato in: moto-uniforme-release.apk"
else
    apksigner sign \
        --ks "$KEYSTORE_PATH" \
        --ks-key-alias "$KEY_ALIAS" \
        --ks-pass "pass:$KEYSTORE_PASS" \
        --key-pass "pass:$KEY_PASS" \
        --out "$SIGNED_APK" \
        "$UNSIGNED_APK"
    echo "APK firmato: moto-uniforme-release.apk"
fi

cd ..

# 5. Instructions
echo ""
echo "[5/5] === ISTRUZIONI PER IL PLAY STORE ==="
echo ""
echo "1. Accedi a https://play.google.com/console"
echo "2. Crea una nuova app"
echo "3. Vai su 'Produzione' > 'Rilasci' > 'Crea nuovo rilascio'"
echo "4. Carica il file: moto-uniforme-release.apk"
echo "   (o usa .aab per Android App Bundle)"
echo "5. Compila scheda store, screenshot, policy e pubblica"
echo ""
echo "Per generare un .aab (preferito dal Play Store):"
echo "  cd android && ./gradlew bundleRelease"
