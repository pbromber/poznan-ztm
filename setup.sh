#!/bin/bash
# Quick setup script for development

echo "🚌 Poznań Transport - Home Assistant Integration"
echo "================================================"
echo ""

# Check if Home Assistant config directory exists
if [ -z "$1" ]; then
    echo "Usage: ./setup.sh /path/to/homeassistant/config"
    echo ""
    echo "Example:"
    echo "  ./setup.sh ~/.homeassistant"
    echo "  ./setup.sh /config  (for Docker/HAOS)"
    exit 1
fi

HA_CONFIG="$1"

if [ ! -d "$HA_CONFIG" ]; then
    echo "❌ Directory $HA_CONFIG does not exist!"
    exit 1
fi

echo "📂 Home Assistant config: $HA_CONFIG"
echo ""

# Install custom component
echo "📦 Installing custom component..."
mkdir -p "$HA_CONFIG/custom_components"
cp -r custom_components/poznan_transport "$HA_CONFIG/custom_components/"
echo "✅ Component installed"

# Install Lovelace card
echo "🎨 Installing Lovelace card..."
mkdir -p "$HA_CONFIG/www"
cp www/poznan-transport-card.js "$HA_CONFIG/www/"
echo "✅ Card installed"

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart Home Assistant"
echo "2. Go to Settings → Devices & Services"
echo "3. Click 'Add Integration'"
echo "4. Search for 'Poznań Public Transport'"
echo "5. Add resource in Settings → Dashboards → Resources:"
echo "   URL: /local/poznan-transport-card.js"
echo "   Type: JavaScript Module"
echo ""
echo "Enjoy! 🚌"

