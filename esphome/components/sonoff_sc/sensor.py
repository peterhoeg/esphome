import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_HUMIDITY,
    CONF_ID,
    CONF_LIGHT,
    CONF_NOISE_LEVEL,
    CONF_PM_10_0,
    CONF_TEMPERATURE,
    CONF_UPDATE_INTERVAL,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    ICON_CHEMICAL_WEAPON,
    ICON_LIGHTBULB,
    ICON_PULSE,
    ICON_THERMOMETER,
    ICON_WATER_PERCENT,
    UNIT_CELSIUS,
    UNIT_PERCENT,
)

DEPENDENCIES = ["uart", "sensor"]

CONF_HUMIDITY_THRESHOLD = "humidity_threshold"
CONF_TEMPERATURE_THRESHOLD = "temperature_threshold"

sonoff_sc_ns = cg.esphome_ns.namespace("sonoff_sc")
SonoffSCComponent = sonoff_sc_ns.class_(
    "SonoffSCComponent", uart.UARTDevice, cg.Component
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(SonoffSCComponent),
            cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                device_class=DEVICE_CLASS_HUMIDITY,
                state_class=STATE_CLASS_MEASUREMENT,
                icon=ICON_WATER_PERCENT,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                icon=ICON_THERMOMETER,
                accuracy_decimals=1,
            ),
            cv.Optional(CONF_LIGHT): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                state_class=STATE_CLASS_MEASUREMENT,
                icon=ICON_LIGHTBULB,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_NOISE_LEVEL): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                state_class=STATE_CLASS_MEASUREMENT,
                icon=ICON_PULSE,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_PM_10_0): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                state_class=STATE_CLASS_MEASUREMENT,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=0,
            ),
            cv.Optional(CONF_UPDATE_INTERVAL, default=60): cv.positive_time_period_seconds,
            cv.Optional(CONF_HUMIDITY_THRESHOLD, default=1): cv.positive_not_null_int,
            cv.Optional(CONF_TEMPERATURE_THRESHOLD, default=1): cv.positive_not_null_int,
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_UPDATE_INTERVAL in config:
        cg.add(var.set_update_interval_sec(config[CONF_UPDATE_INTERVAL]))

    if CONF_HUMIDITY_THRESHOLD in config:
        cg.add(var.set_humidity_threshold(config[CONF_HUMIDITY_THRESHOLD]))

    if CONF_TEMPERATURE_THRESHOLD in config:
        cg.add(var.set_temperature_threshold(config[CONF_TEMPERATURE_THRESHOLD]))

    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(sens))

    if CONF_HUMIDITY in config:
        sens = await sensor.new_sensor(config[CONF_HUMIDITY])
        cg.add(var.set_humidity_sensor(sens))

    if CONF_LIGHT in config:
        sens = await sensor.new_sensor(config[CONF_LIGHT])
        cg.add(var.set_light_sensor(sens))

    if CONF_NOISE_LEVEL in config:
        sens = await sensor.new_sensor(config[CONF_NOISE_LEVEL])
        cg.add(var.set_noise_sensor(sens))

    if CONF_PM_10_0 in config:
        sens = await sensor.new_sensor(config[CONF_PM_10_0])
        cg.add(var.set_dust_sensor(sens))
