PiSPEC 3.0

abstract class SWITCH {
inherit PROTECTION_OBJECT PROTECTED_OBJECT;

Variables:
  sw, sw1;

Inputs:

  """
  Input from the wayside. The switch is detected in the normal position.
  """
  DetectedNormal;

  """
  Input from the wayside. The switch is detected in the reverse position.
  """
  DetectedReverse;

  """
  Input from the office system. The switch is requested in the normal position.
  """
  RequestedNormal;

  """
  Input from the office system. The switch is requested in the reverse position.
  """
  RequestedReverse;

Parameters:

  """ The right leg is the straight leg (as the symbol is drawn). """
  bool right_straight;

Functions: // Static

  """
  The track in which the switch is contained.
  """
  bool track(TRACK_CIRCUIT tc) :=
    objects(tc, SELF);

Functions: // Dynamic

  """
  The switch is locked when it is contained in a locked route section or
  the track containing the switch is occupied.
  """
  bool locked;

  """
  The switch is in normal correspondence.
  """
  bool correspondence_normal;

  """
  The switch is in reverse correspondence.
  """
  bool correspondence_reverse;

Equations:

  """
  The switch is commanded in the normal position, i.e. the last accepted
  request was for the normal position.
  """
  CommandedNormal;

  """
  The switch is commanded in the reverse position, i.e. the last accepted
  request was for the reverse position.
  """
  CommandedReverse;

  """
  Output to the switch motor. The motor is ordered to move the switch to the
  normal position.

  Note: the order will only be sent until the relevant timer times out.
  """
  MoveNormal;

  """
  Output to the switch motor. The motor is ordered to move the switch to the
  reverse position.

  Note: the order will only be sent until the relevant timer times out.
  """
  MoveReverse;

Outputs:

  MoveNormal;
  MoveReverse;

Attributes:

  InteractiveType : RequestedReverse["Pulse 0.5, Toggle"];
  InteractiveType : RequestedNormal["Pulse 0.5, Toggle"];

  NormalValue : RequestedReverse["False"];
  NormalValue : RequestedNormal["False"];

Functions: // Normal values

  bool normal__DetectedNormal := SELF.CommandedNormal;
  bool normal__DetectedReverse := SELF.CommandedReverse;

}
