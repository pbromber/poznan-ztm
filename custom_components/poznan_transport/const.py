"""Constants for the Poznań Public Transport integration."""

DOMAIN = "poznan_transport"

# API Configuration
API_URL = "https://www.peka.poznan.pl/vm/method.vm"
API_TIMEOUT = 10

# Update interval
UPDATE_INTERVAL = 30  # seconds

# Config entry keys
CONF_STOP_SYMBOL = "stop_symbol"
CONF_STOP_NAME = "stop_name"
CONF_LINES = "lines"

# Attributes
ATTR_LINE = "line"
ATTR_DIRECTION = "direction"
ATTR_MINUTES = "minutes"
ATTR_DEPARTURE = "departure"
ATTR_REAL_TIME = "real_time"
ATTR_VEHICLE = "vehicle"
ATTR_BIKE = "bike"
ATTR_AIR_CONDITIONING = "air_conditioning"
ATTR_LOW_FLOOR = "low_floor"
ATTR_STOP_NAME = "stop_name"
ATTR_STOP_SYMBOL = "stop_symbol"

