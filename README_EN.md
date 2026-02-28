# ha-ixcommand

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant custom component for iXcommand EV Chargers. Control your EV charger and monitor charging sessions with full integration into Home Assistant's Energy Dashboard.

## Features

- **Complete Control**: Turn charging on/off, set current limits, configure boost settings
- **Real-time Monitoring**: Track charging power, current, energy consumption, and status
- **Energy Dashboard Integration**: Automatic inclusion of energy consumption data
- **Multiple Chargers**: Add as many chargers as needed (each as a separate integration)
- **WiFi Diagnostics**: Monitor signal strength, SSID, and connection status

## Installation

### Option 1: HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed
2. Add this repository as a custom repository in HACS:
   - Go to HACS → Integrations
   - Click the three dots (⋮) → Custom repositories
   - Add `https://github.com/legendik/ha-ixcommand` as a repository URL
   - Select "Integration" as category
3. Search for "iXcommand EV Charger" and install it
4. Restart Home Assistant

### Option 2: Manual Installation

1. Download the `custom_components/ixcommand/` folder from this repository
2. Copy it to your Home Assistant's `custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "iXcommand EV Charger" and select it
3. Enter your:
   - **API Key**: Your iXcommand API key
   - **Serial Number**: Your charger serial number (format: XXX-XXX-XXX)
4. Click **Submit**

### Getting API Key and Serial Number

1. Log in to https://www.ixfield.com/app/account
2. Generate a new API key in the API section
3. The serial number is on the label on the back of the charger (marked S/N)
   - Format: XXX-XXX-XXX (e.g., ABC-123-DEF)

### Adding Multiple Chargers

To add another charger:
1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "iXcommand EV Charger" again
3. Enter the API key and serial number for the second charger
4. Each charger will appear as a separate device in Home Assistant

## Entities

Each charger creates the following entities:

### Sensors
- **Current Charging Power** (`sensor`): Real-time charging power in watts
- **Total Energy** (`sensor`): Lifetime energy consumption in watt-hours (available in Energy Dashboard)
- **Charging Current L1/L2/L3** (`sensor`): Current per phase in amperes
- **Boost Remaining** (`sensor`): Remaining boost time in seconds
- **WiFi Signal** (`sensor`): WiFi signal strength percentage
- **Charging Status** (`sensor`): Current charging state (INIT/IDLE/CONNECTED/CHARGING/etc.)
- **WiFi SSID** (`sensor`): Connected WiFi network name
- **WiFi BSSID** (`sensor`): WiFi access point MAC address

### Switches
- **Charging Enable** (`switch`): Turn charging on/off
- **Single Phase Mode** (`switch`): Toggle between 1-phase and 3-phase charging
- **Boost Mode** (`switch`): Current boost status (read-only)

### Number Controls
- **Target Current** (`number`): Set normal charging current (6-16A, depending on max current)
- **Boost Current** (`number`): Set boost charging current (6-16A, depending on max current)
- **Maximum Current** (`number`): Set maximum allowed current (6-16A)
- **Boost Time** (`number`): Set boost duration (0-86400 seconds)

## Energy Dashboard

The **Total Energy** sensor is automatically configured for the Home Assistant Energy Dashboard:
- Device Class: `energy`
- State Class: `total_increasing`
- Unit: `Wh`

To add it to your Energy Dashboard:
1. Go to **Settings** → **Dashboards** → **Energy**
2. Under "Individual Devices", click **Add Device**
3. Select your iXcommand charger device
4. The energy consumption will be tracked automatically

## API Information

This integration uses the iXcommand API at `https://evcharger.ixcommand.com/api/v1/`. The API requires:
- **Authentication**: X-API-KEY header
- **Endpoints**: `/thing/{serial}/properties` for reading/writing charger properties
- **Polling**: 30-second intervals to minimize API load

## Troubleshooting

### Connection Issues
- Verify your API key is correct
- Check that your serial number is in XXX-XXX-XXX format
- Ensure your charger is online and connected to the internet

### Authentication Errors
- Your API key may be invalid or expired
- Use the re-authentication flow in Home Assistant to update credentials

### Missing Entities
- Restart Home Assistant after installation
- Check Home Assistant logs for any error messages

## Support

For issues or feature requests, please create an issue on this GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
