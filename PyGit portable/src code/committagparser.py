import collections

# Parsing code comes from https://wyag.thb.lt/#orgc8b86d2
def parse_committag(raw, start = 0, dict=None):
    """Recursively reads key/value pairs from a commit message or tag"""
    if not dict:
        dict = collections.OrderedDict() # OrderedDict to maintain message order correctly for reserialising

    # Find newline and space to determine position
    space = raw.find(b' ', start)
    newline = raw.find(b'\n', start)

    # Blank line check (no space or space after newline means not a message)
    if (space < 0) or (newline < space):
        dict[None] = raw[start+1:] # Store blank line position
        return dict

    # Otherwise it's a proper key,value pair and we read it
    key = raw[start:space]

    # Find the end of the value.  Continuation lines begin with a
    # space, so we loop until we find a "\n" not followed by a space.
    end = start
    while True:
        end = raw.find(b'\n', end+1)
        if raw[end+1] != ord(' '): break

    # Grab the value
    # Also, drop the leading space on continuation lines
    value = raw[space+1:end].replace(b'\n ', b'\n')

    # Don't overwrite existing data contents
    if key in dict:
        if type(dct[key]) == list:
            dict[key].append(value)
        else:
            dict[key] = [ dct[key], value ]
    else:
        dict[key]=value

    return parse_committag(raw, start=end+1, dict=dict)

def serialise_committag(committag):
    ret = b''

    # Output fields
    for k in committag.keys():
        # Skip the message itself
        if k == None: continue
        val = committag[k]
        # Normalize to a list
        if type(val) != list:
            val = [ val ]

        for v in val:
            ret += k + b' ' + (v.replace(b'\n', b'\n ')) + b'\n'

    # Append message
    ret += b'\n' + committag[None] + b'\n'

    return ret
