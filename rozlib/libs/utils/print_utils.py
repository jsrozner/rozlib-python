from pprint import pp

# Print all properties of the object
def print_obj(obj):
    for attr in dir(obj):
        # Ignore built-in attributes and methods
        if attr.startswith("__"):
            continue
        try:
            # Get the value of the attribute or property
            value = getattr(obj, attr)
            print(f"{attr}: {pp.pformat(value)}")
        except Exception as e:
            print(f"{attr}: Error accessing value ({e})")
