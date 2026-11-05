PiSPEC 3.0

class GDS_ROUTE {
inherit ROUTE;

Functions:

bool ready_to_lock :=
  SELF.RouteRequested &
  SELF.protected_flank &
  SELF.protected_front &
  ALL rts:SELF.conflicting_route_section ~rts.Locked &
  ALL tc:SELF.tracks tc.Clear &
  ALL sw:SELF.switches_normal sw.correspondence_normal &
  ALL sw:SELF.switches_reverse sw.correspondence_reverse;

  bool ready_to_proceed :=
  SELF.set &
  SELF.protected_flank &
  SELF.protected_front &
  ALL tc:SELF.tracks tc.Clear &
  ALL sw:SELF.switches_normal sw.correspondence_normal &
  ALL sw:SELF.switches_reverse sw.correspondence_reverse;

  bool protected_front :=
    SELF.ends_at_buffer_stop #
    SOME esi:SELF.end_object (
      esi.LineInput &
      SOME tc:esi.track_after tc.Clear
    ) #
    SOME si:SELF.end_object
    SOME pa (
      protects_signal(pa, si) &
      protective(pa)
    );

  bool protected_flank :=
    ALL sw:SELF.switches_normal
    SOME pa (
      protects_sw_normal(pa, sw) &
      protective(pa)
    ) &
    ALL sw:SELF.switches_reverse
    SOME pa (
      protects_sw_reverse(pa, sw) &
      protective(pa)
    );


Equations:

"""
  The release timer input: a manual release is requested for a route that is
  locked, and no immediate release applies.
  """
  ReleaseTimer :=
    SELF.ReleaseRequested &
    (ALL rts:SELF.route_sections rts.Locked) &
    ~SELF.immediate_manual_release;

Timers:

  ReleaseTimer (SET=0 SEC, CLEAR=30 SEC, FIXED);
}
