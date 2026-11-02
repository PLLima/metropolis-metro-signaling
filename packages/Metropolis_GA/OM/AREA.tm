PiSPEC 3.0

abstract class AREA {

Parameters:

  """
  Objects in or on the border of the area.
  """
  set<OBJECT> objects;

  """
  Areas sharing at least one edge with this area.
  """
  set<AREA> intersects_by_edge;

  """
  Areas sharing at least one node with this area.
  """
  set<AREA> intersects_by_node;

}
