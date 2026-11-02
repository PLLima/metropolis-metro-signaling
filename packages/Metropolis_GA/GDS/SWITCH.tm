PiSPEC 3.0

class GDS_SWITCH {
inherit SWITCH;

Functions: // Dynamic

  """
  The switch is locked when it is contained in a locked route section or
  the track containing the switch is occupied.
  """
  bool locked :=
    SOME rts (
      objects(rts, SELF) &
      rts.Locked
    ) #
    SOME tc:SELF.track ~tc.Clear;

  """
  The switch is in normal correspondence.
  """
  bool correspondence_normal :=
    SELF.CommandedNormal &
    SELF.DetectedNormal &
    ~SELF.DetectedReverse;

  """
  The switch is in reverse correspondence.
  """
  bool correspondence_reverse :=
    SELF.CommandedReverse &
    SELF.DetectedReverse &
    ~SELF.DetectedNormal;

  """
  A request for normal position is accepted.
  """
  bool accept_normal_request :=
    SELF.RequestedNormal & ~SELF.RequestedReverse &
    ~SELF.locked & ~SELF.protects_sw &
    ~SELF.protects_signal;

  """
  A request for reverse position is accepted.
  """
  bool accept_reverse_request :=
    SELF.RequestedReverse & ~SELF.RequestedNormal &
    ~SELF.locked & ~SELF.protects_sw &
    ~SELF.protects_signal;

  """
  The switch starts to move to the normal postition.
  """
  bool start_move_normal :=
    ~SELF.PreCommandedNormal & SELF.CommandedNormal;

  """
  The switch starts to move to the reverse postition.
  """
  bool start_move_reverse :=
    ~SELF.PreCommandedReverse & SELF.CommandedReverse;

  """
  The switch protects another switch that lies in a locked route section.
  """
  bool protects_sw :=
    SOME sw
    SOME rts
    SOME pa (
      objects(rts, sw) &
      Locked(rts) &
      protective(pa) & (
        switches_normal(pa, SELF) #
        switches_reverse(pa, SELF)
      ) & (
        switches_normal(rts, sw) &
        protects_sw_normal(pa, sw) #
        switches_reverse(rts, sw) &
        protects_sw_reverse(pa, sw)
      )
    );

  """
  The switch protects a signal that is end locked and is not commanded to
  proceed.
  """
  bool protects_signal :=
    SOME si
    SOME pa
    SOME sw (
      protects_signal(pa, si) & (
        switches_normal(pa, SELF) #
        switches_reverse(pa, SELF)
      ) &
      end_locked(si) &
      protective(pa) &
      ~CommandedProceed(si)
    );

Equations:

  """
  At startup, the interlocking will assume the commanded position to be
  the detected position. After a commanded position has been registered,
  this function is turned off.
  """
  Initialized :=
    SELF.CommandedNormal #
    SELF.CommandedReverse #
    SELF.Initialized;

  """
  The switch was commanded normal in the previous cycle.
  """
  PreCommandedNormal := SELF.CommandedNormal;

  """
  The switch was commanded reverse in the previous cycle.
  """
  PreCommandedReverse := SELF.CommandedReverse;

  CommandedNormal :=
    // Initialization
    ~SELF.Initialized &
    ~SELF.CommandedNormal &
    ~SELF.CommandedReverse &
    ~SELF.RequestedNormal &
    ~SELF.RequestedReverse &
    SELF.DetectedNormal &
    ~SELF.DetectedReverse #
    // Normal request
    SELF.accept_normal_request #
    SELF.CommandedNormal & ~SELF.CommandedReverse &
    ~SELF.accept_reverse_request;

  CommandedReverse :=
    // Initialization
    ~SELF.Initialized &
    ~SELF.CommandedNormal &
    ~SELF.CommandedReverse &
    ~SELF.RequestedNormal &
    ~SELF.RequestedReverse &
    SELF.DetectedReverse &
    ~SELF.DetectedNormal #
    // Reverse request
    SELF.accept_reverse_request #
    SELF.CommandedReverse & ~SELF.CommandedNormal &
    ~SELF.accept_normal_request;

  MoveNormal :=
    SELF.CommandedNormal & ~SELF.DetectedNormal &
    (SELF.start_move_normal # SELF.MoveNormal) &
    ~SELF.NormalTimeout;

  """
  The timer for normal movement has timed out. The switch motor will not be
  ordered to move.
  """
  NormalTimeout := SELF.MoveNormal;

  MoveReverse :=
    SELF.CommandedReverse & ~SELF.DetectedReverse &
    (SELF.start_move_reverse # SELF.MoveReverse) &
    ~SELF.ReverseTimeout;

  """
  The timer for reverse movement has timed out. The switch motor will not be
  ordered to move.
  """
  ReverseTimeout := SELF.MoveReverse;

Timers:

  NormalTimeout (SET = 5 SEC, CLEAR = 0 MSEC, FIXED);
  ReverseTimeout (SET = 5 SEC, CLEAR = 0 MSEC, FIXED);

}
