# Poznań Public Transport - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

English version | [Wersja polska](README.md)

Home Assistant integration for public transport in Poznań, Poland (ZTM Poznań / PEKA).

## Features

- 🚌 Real-time schedule display
- 📍 Support for multiple stops
- 🔍 Filter by bus/tram lines
- ♿ Accessibility information (air conditioning, low floor, bike racks)
- 🎨 Beautiful Lovelace card with icons
- ⚡ Auto-refresh every 30 seconds

## Installation

### Method 1: HACS (recommended)

1. Open HACS in Home Assistant
2. Click "Integrations"
3. Click the menu (3 dots) and select "Custom repositories"
4. Add URL: `https://github.com/pbromber/ztm-hass`
5. Select category: "Integration"
6. Click "Add"
7. Find "Poznań Public Transport" and click "Download"
8. Restart Home Assistant

### Method 2: Manual

1. Copy the entire `custom_components/poznan_transport` folder to `config/custom_components/poznan_transport` in Home Assistant
   - The card file (`poznan-transport-card.js`) is already in this folder and will be automatically copied to `www/community/poznan-transport-card/` on first run
2. Restart Home Assistant
3. The integration will automatically copy the Lovelace card to `config/www/community/poznan-transport-card/`

## Configuration

### Adding a stop

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Poznań Public Transport**
4. Enter:
   - **Stop Symbol** - stop code (e.g., `NIED01`)
   - **Lines** (optional) - lines to filter, comma-separated (e.g., `171, 172, 173`)

### How to find the stop code?

1. Go to https://www.peka.poznan.pl/vm/
2. Select your stop from the list
3. The stop code is usually the first few letters of the name + pole number
4. Examples:
   - `RONDO01` - Rondo Kaponiera
   - `DWOR01` - Main Railway Station

## Sensors

After adding a stop, 2 sensors will be created:

### 1. Next Departure
- **Entity ID**: `sensor.{stop}_next_departure`
- **State**: Next departure (e.g., "Line 171 - 5 min")
- **Attributes**:
  - `line` - line number
  - `direction` - direction of travel
  - `minutes` - minutes until departure
  - `departure` - exact departure time
  - `real_time` - whether it's real-time data (true/false)
  - `vehicle` - vehicle number
  - `bike` - bike rack available
  - `air_conditioning` - air conditioning
  - `low_floor` - low floor

### 2. All Departures
- **Entity ID**: `sensor.{stop}_all_departures`
- **State**: Number of upcoming departures
- **Attributes**:
  - `departures` - list of all departures (max 10)

## Lovelace Card

### Adding the card

1. Add resource in **Settings** → **Dashboards** → **Resources**:
   ```
   URL: /local/community/poznan-transport-card/poznan-transport-card.js
   Type: JavaScript Module
   ```

2. Add card to dashboard:
   - Open your dashboard in Home Assistant
   - Click **Edit Dashboard** (pencil icon in top right corner)
   - Click **Add Card** (blue button at the bottom)
   - Scroll down and select **Manual** (manual configuration)
   - Paste the following YAML:
   ```yaml
   type: custom:poznan-transport-card
   entity: sensor.niedziałkowskiego_all_departures
   max_departures: 5
   ```
   - Click **Save**, then **Done**

### Card options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `entity` | string | Yes | Entity ID of "All Departures" sensor |
| `max_departures` | number | No | Maximum number of departures to display (default: 5) |

### Example configuration

```yaml
type: custom:poznan-transport-card
entity: sensor.niedziałkowskiego_all_departures
max_departures: 8
```

## Usage Examples

### Simple sensor in dashboard

```yaml
type: entities
entities:
  - entity: sensor.niedziałkowskiego_next_departure
    name: Next bus
```

### Card with multiple stops

```yaml
type: vertical-stack
cards:
  - type: custom:poznan-transport-card
    entity: sensor.niedziałkowskiego_all_departures
    max_departures: 5
  - type: custom:poznan-transport-card
    entity: sensor.rondo_kaponiera_all_departures
    max_departures: 3
```

### Automation - bus notification

```yaml
automation:
  - alias: "Bus notification"
    trigger:
      - platform: state
        entity_id: sensor.niedziałkowskiego_next_departure
    condition:
      - condition: template
        value_template: "{{ state_attr('sensor.niedziałkowskiego_next_departure', 'minutes') == 5 }}"
      - condition: template
        value_template: "{{ state_attr('sensor.niedziałkowskiego_next_departure', 'line') == '171' }}"
    action:
      - service: notify.mobile_app
        data:
          title: "Bus 171"
          message: "Departing in 5 minutes!"
```

### Conditional card - show only when bus is coming

```yaml
type: conditional
conditions:
  - entity: sensor.niedziałkowskiego_next_departure
    state_not: "No departures"
card:
  type: custom:poznan-transport-card
  entity: sensor.niedziałkowskiego_all_departures
  max_departures: 3
```

## Troubleshooting

### Integration not visible in "Add Integration"

1. Restart Home Assistant
2. Clear browser cache (Ctrl+Shift+R)
3. Check logs: **Settings** → **System** → **Logs**

### Card not displaying / "Custom element doesn't exist: poznan-transport-card"

1. **Check if card file exists in Home Assistant:**
   - File must be in `config/www/community/poznan-transport-card/poznan-transport-card.js`
   - When installed via HACS, the file is copied automatically after restart
2. **Add resource:** **Settings** → **Dashboards** → **Resources**
   - URL: `/local/community/poznan-transport-card/poznan-transport-card.js`
   - Type: JavaScript Module
3. **Clear browser cache:** Ctrl+Shift+R (or Cmd+Shift+R on Mac)
4. **Restart Home Assistant**
5. Check developer console (F12) in browser - are there any file loading errors

### "Invalid stop symbol"

1. Check if the stop code is correct
2. Make sure it's written in UPPERCASE
3. Try a different stop (e.g., `NIED01`)

### Data not refreshing

1. Check Home Assistant internet connection
2. ZTM Poznań API may be temporarily unavailable
3. Check integration logs

## Technical

- **API**: https://www.peka.poznan.pl/vm/method.vm
- **Update**: Every 30 seconds
- **Timeout**: 10 seconds
- **Platform**: Sensor
- **Requirements**: Home Assistant 2023.1+

## License

MIT License

## Author

Created by [@pbromber](https://github.com/pbromber)

## Support

If you like this integration, leave a ⭐ on GitHub!

Found a bug? [Report an issue](https://github.com/pbromber/ztm-hass/issues)
