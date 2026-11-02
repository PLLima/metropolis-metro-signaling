PiSPEC 3.0

abstract class APPROACH_PATH {
inherit PATH;

Parameters:

  """
  The signal to which this approach path is related to.
  """
  SIGNAL end_signal;


Variables:
  ap;

Equations:

  """
  A track circuit belonging to this approach path is occupied 
  and the in-between switches are in correspondence with the path.
  """
  Incoming;
  
}