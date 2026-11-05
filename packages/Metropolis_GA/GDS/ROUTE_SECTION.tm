PiSPEC 3.0

class GDS_ROUTE_SECTION {
inherit ROUTE_SECTION;

Functions:
  """
  The route section is clear from occupancy.
  """
  bool clear :=
    ALL tc:SELF.tracks tc.Clear;

  """
  The route section releases if it has been occupied and now
  is clear from occupancy.
  """
  bool release :=
    SELF.clear &
    SELF.ReadyToRelease;

  """
  The track section is commanded to lock by a route that contains it.
  """
  bool lock_commanded :=
    SOME rt (
      rt.ready_to_lock & route_sections(rt, SELF)
    );

  """
  It is true when a containing route has just been manually unlocked
  """
  bool manual_unlocking :=
    SOME rt (
      route_sections(rt, SELF) &
      rt.JustUnlocked &
      ~SOME rt1 (
        ~(rt1 = rt) &
        route_sections(rt1, SELF) & (
          rt1.Holding & ~rt1.JustUnlocked #
          rt1.ready_to_lock
        )
      )
    );

Equations:
  """
  A route section becomes locked if commanded to lock. It stays locked
  until the release conditions are fulfilled.
  """
  Locked :=
    (SELF.lock_commanded # SELF.Locked) &
    ~SELF.release &
    ~SELF.manual_unlocking;

  """
  A route section becomes ready to release if it is occupied. It stays ready to
  release until it releases.
  """
  ReadyToRelease :=
    SELF.Locked & (
      ~SELF.clear #
      SELF.ReadyToRelease
    );

}
