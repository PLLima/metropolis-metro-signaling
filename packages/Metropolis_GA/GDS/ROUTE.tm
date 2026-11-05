PiSPEC 3.0

class GDS_ROUTE {
inherit ROUTE;

Functions:
// Not blocked by a running release timer: a route re-requested during the countdown stays
// unset (start signal at stop) and is released anyway when the timer expires.
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
    // Note: si also ranges over exit signals, unlike GSS_06. No station has a
    // protection area for an exit signal.
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
    SOME rts:SELF.route_sections rts.Locked &
    // Ignore the request if another set route shares a route section with this one,
    // so that the shared section is never released under the other route.
    ~SOME rt1 (
      ~(rt1 = SELF) &
      set(rt1) &
      SOME rts:SELF.route_sections route_sections(rt1, rts)
    ) &
    ~SELF.immediate_manual_release;

  Holding :=
    SELF.ready_to_lock #
    SELF.Holding &
    SOME rts:SELF.route_sections rts.Locked &
    ~SELF.JustUnlocked;

Timers:
  // Off-delay: runs while the request is held and 30 s after it ends.
  // The request is a pulse, so the release happens about 30.5 s after it is received.
  ReleaseTimer (SET=0 SEC, CLEAR=30 SEC, FIXED);
}
