from cspkg.core import Command

@Command()
def lower(xstr):
    """
    """

    map  = xstr.tag_ranges('sel')
    for index in range(0, len(map) - 1, 2):
        xstr.swap(xstr.get(map[index], 
            map[index + 1]).lower(), map[index], map[index + 1])

@Command()
def upper(xstr):
    """
    """

    map  = xstr.tag_ranges('sel')
    for index in range(0, len(map) - 1, 2):
        xstr.swap(xstr.get(map[index], 
            map[index + 1]).upper(), map[index], map[index + 1])



