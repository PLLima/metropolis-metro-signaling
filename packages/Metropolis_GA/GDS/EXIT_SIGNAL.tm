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
    ~end_locked(SELF) &
    ~CommandedProceed(SELF) &
    SOME tc:SELF.track_after tc.Clear;

  """
  Requirement EXIT 2: the exit signal is commanded to proceed only when it is
  end locked, the line input from the neighbouring station is set and the
  line track circuit is vacant.
  """
  CommandedProceed :=
    end_locked(SELF) &
    SELF.LineInput &
    SOME tc:SELF.track_after tc.Clear;

}
