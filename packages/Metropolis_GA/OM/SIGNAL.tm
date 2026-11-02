PiSPEC 3.0

abstract class SIGNAL {
inherit PROTECTION_OBJECT PROTECTED_OBJECT ROUTE_END;

Variables:
  si, si1;

Inputs:

  """
  Input from wayside. The signal shows proceed.
  """
  ShowsProceed;

Equations:

  """
  The signal is commanded to show proceed.
  For non-exit signals, this happens when there is a route starting at the
  signal that is ready to proceed.
  For exit signals, this happens when the signal is endlocked and the track
  circuit behind it is clear of occupancy.
  """
  CommandedProceed;

Outputs:

  CommandedProceed;

Parameters:

  """
  The track immediately after the signal.
  """
  TRACK_CIRCUIT track_after;

  """
  The track immediately before the signal.
  """
  TRACK_CIRCUIT track_before;

Functions:

  """
  Routes starting in this signal.
  """
  bool routes(ROUTE rt) :=
    start_signal(rt, SELF);

  """
  This signal is an exit signal, i.e. there is no route starting in this signal.
  """
  bool exit_signal :=
   ~SOME rt:SELF.routes true;

  """
  This signal is end locked; i.e. it is the end signal of a route whose last
  route section is locked.
  """
  bool end_locked :=
    SOME rt
    SOME rts (
      end_object(rt, SELF) &
      last_route_section(rt, rts) &
      Locked(rts)
    );

Functions: // Normal values

  bool normal__ShowsProceed := SELF.CommandedProceed;

}
