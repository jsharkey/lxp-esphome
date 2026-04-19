
import csv
import io
import sys

sensors = io.StringIO()
text_sensors = io.StringIO()

reader = csv.DictReader(sys.stdin, delimiter='\t')
for row in reader:
  if row["value_type"].startswith("RAW"):
    buf = text_sensors
  else:
    buf = sensors

  buf.write("\n  - platform: modbus_controller")
  buf.write("\n    modbus_controller_id: inverter_1")
  buf.write("\n    id: %s" % (row["id"]))
  buf.write("\n    name: '%s'" % (row["name"]))
  if row["internal"] == "TRUE":
    buf.write("\n    internal: true")
  buf.write("\n    register_type: read")
  buf.write("\n    address: %s" % (row["address"]))
  if row["value_type"].startswith("RAW"):
    count = 2 if "DWORD" in row["value_type"] else 1
    buf.write("\n    register_count: %d" % (count))
    buf.write("\n    raw_encode: HEXBYTES")
  else:
    buf.write("\n    value_type: %s" % (row["value_type"]))
  if row["state_class"]:
    buf.write("\n    state_class: '%s'" % (row["state_class"]))
  if row["device_class"]:
    buf.write("\n    device_class: %s" % (row["device_class"]))
  if row["unit_of_measurement"]:
    buf.write("\n    unit_of_measurement: '%s'" % (row["unit_of_measurement"]))
  if row["entity_category"]:
    buf.write("\n    entity_category: '%s'" % (row["entity_category"]))
  if row["multiply"] and row["multiply"] != "1":
    buf.write("\n    accuracy_decimals: %d" % (row["multiply"].count("0")))
    buf.write("\n    filters:")
    buf.write("\n      - multiply: %s" % (row["multiply"]))
  elif row["unit_of_measurement"] == "°C":
    buf.write("\n    filters:")
    buf.write("\n      - filter_out: 0")


sys.stdout.write("\nsensor:")
sys.stdout.write(sensors.getvalue())
sys.stdout.write("\ntext_sensor:")
sys.stdout.write(text_sensors.getvalue())
