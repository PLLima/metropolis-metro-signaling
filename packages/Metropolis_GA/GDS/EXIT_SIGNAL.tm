PiSPEC 3.0

class GDS_EXIT_SIGNAL {
inherit EXIT_SIGNAL;

Equations:
  """
  The line output is true when this interlocking is not using the line: no
  route ending at this exit signal is set, and the line track circuit is
  clear of occupancy. The neighbouring interlocking may then let trains
  enter the line.
  """
  LineOutput :=
    ~SOME rt (
      end_object(rt, SELF) &
      set(rt)
    ) &
    ALL tc:SELF.track_after tc.Clear;

  CommandedProceed :=
    false;

}
