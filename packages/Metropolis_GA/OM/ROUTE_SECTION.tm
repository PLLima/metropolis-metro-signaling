PiSPEC 3.0

abstract class ROUTE_SECTION {
inherit PATH;

Variables:
  rts, rts1, rts2;

Functions:

  """
  Check if a route containing this route section has just unlocked
  - this either happens 30 seconds after the parent route receives its manual
  release request, or immediately based on certain conditions.
  """
  bool manual_unlocking;

Equations:

  """
  A route section becomes locked if commanded to lock. It stays locked
  until the release conditions are fulfilled.
  """
  Locked;

  """
  A route section becomes ready to release if it is occupied. It stays ready to
  release until it releases.
  """
  ReadyToRelease;

Attributes:

  NormalValue : Locked["False"];

}
