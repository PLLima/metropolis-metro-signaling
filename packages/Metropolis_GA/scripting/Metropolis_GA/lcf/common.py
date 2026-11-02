import PiSpecAPI

def get_mirror_type_name(om_type_name, mirror_types, prefix):
    """
    This function returns the name of the "mirror" type for a given OM
    type. The "mirror" types are typically GVS or GTS types that
    mirror (or almost mirror) the OM types. For example, for the OM
    class SWITCH there is typically a GVS_SWITCH and a GTS_SWITCH
    class.

    The GVS/GTS is often more abstract than the OM. E.g. all main
    signals may be using the same visualization/test class. Given a
    named OM type, this function returns the name of the mirror class
    that should be instantiated instead. This is the first class
    that matches when adding _prefix_ to the OM name, the name of the
    OM super class, the super super class, etc.
    """
    # Simple case; prefix + OM type name
    dest_type_name = prefix + om_type_name
    if dest_type_name in mirror_types:
        return dest_type_name

    # Start digging through superclasses for a match prefix + OM superclass name
    super_class_dict = dict()
    for c in PiSpecAPI.GDSClasses:
        for s in (s.Name for s in c.Subclasses()):
            if s not in super_class_dict:
                super_class_dict[s] = list()
            super_class_dict[s].append(c.Name)
    curr_type = om_type_name
    while curr_type in super_class_dict:
        curr_type = super_class_dict[curr_type][0]
        dest_type_name = prefix + curr_type
        if dest_type_name in mirror_types:
            return dest_type_name

    # No mirror type exists
    return None
