PiSPEC 3.0

abstract class ROUTE {
inherit PATH;

Variables:
  rt, rt1, rt2;

Parameters:

  """
  Starting signal of the route.
  """
  SIGNAL start_signal;

  """
  End object of the route.
  """
  ROUTE_END end_object;

Inputs:

  """
  The route is requested. Input from the office system.
  """
  RouteRequested;

  """
  Manual release of the route is requested. Input from the office system.
  When received, the start signal of the route stops being commanded to
  proceed and the 30s release timer starts. When the timer has expired, all
  route sections of the route are released simultaneously.
  """
  ReleaseRequested;
  
Functions: // Static

  """
  A route section rts is conflicting with the route if rts shares a track
  circuit with the route, but rts is not part of the route.
  """
  bool conflicting_route_section(ROUTE_SECTION rts) :=
    SOME tc:SELF.tracks (
      ~route_sections(SELF, rts) &
      tracks(rts, tc)
    );

  """
  The track immediately before the route.
  """
  bool berth_track(TRACK_CIRCUIT tc) :=
    SOME si:SELF.start_signal objects(tc, si) &
    ~tracks(SELF, tc);

  """
  The track immediately after the route.
  """
  bool track_after(TRACK_CIRCUIT tc) :=
    SOME si:SELF.end_object objects(tc, si) &
    ~tracks(SELF, tc);

  """
  Route sections in the route.
  """
  bool route_sections(ROUTE_SECTION rts) :=
    subpath(SELF, rts);

  """
  The last route section in the route.
  """
  bool last_route_section(ROUTE_SECTION rts) :=
    route_sections(SELF, rts) &
    ~SOME rts1:SELF.route_sections (
      follows(rts, rts1)
    );

  """
  All protection areas for the route (flank and front protections).
  """
  bool protection_areas(PROTECTION_AREA pa) :=
    SOME sw:SELF.switches_normal protects_sw_normal(pa, sw) #
    SOME sw:SELF.switches_reverse protects_sw_reverse(pa, sw) #
    SOME si:SELF.end_object protects_signal(pa, si);

  """
  The route ends at an exit signal.
  """
  bool ends_at_exit_signal :=
    SOME esi:SELF.end_object true;

  """
  The route can release immediately upon receiving a manual request,
  if it is not occupied and no trains are detected in the approach
  paths of its start signal.
  """
  bool immediate_manual_release := false;

  """
  The route ends at a buffer stop.
  """
  bool ends_at_buffer_stop :=
    SOME bs:SELF.end_object true;

Functions: // Dynamic

  """
  The route is set, i.e. all its route sections are locked and the manual
  release timer is not running.
  """
  bool set :=
    (ALL rts:SELF.route_sections rts.Locked) &
    ~SELF.ReleaseTimer;

  """
  The route is ready to lock. This will lock all its route sections and
  command its start signal to proceed.
  """
  bool ready_to_lock;

  """
  The route is ready to proceed, meaning
  * it is set and
  * it has flank protected and
    - it has front protection, or
    - the end signal is commanded proceed, and
  * it is clear of obstacles and
  * all its switches are in correspondance in their right positions.
  """
  bool ready_to_proceed;

  """
  The front of the route is protected.
  """
  bool protected_front;

  """
  The flank of the route is protected.
  """
  bool protected_flank;

Equations:

  """
  The route stops being locked by a manual release request and will 
  force its route sections to do the same. This either happens after
  the 30s release timer has expired, or immediately, based on certain conditions.
  """
  //Ordering of equations matters when trying to use this for 
  //previous cycle memory.
  bool JustUnlocked := 
    (SELF.PreReleaseTimer & ~SELF.ReleaseTimer) #
    SELF.immediate_manual_release;
  
  """
  The 30s timer for manual release was active in the previous cycle.
  """
  bool PreReleaseTimer := SELF.ReleaseTimer;

  """
  The 30s timer for manual release is active. It starts when ReleaseRequested
  is received, unless the immediate release conditions are satisfied, and
  stops after 30 seconds. While it is active the route is not set.
  """
  bool ReleaseTimer;

Attributes:

  InteractiveType : RouteRequested["Pulse 0.5, Toggle"];
  InteractiveType : ReleaseRequested["Pulse 0.5, Toggle"];

  NormalValue : RouteRequested["False"];
  NormalValue : ReleaseRequested["False"];

}
