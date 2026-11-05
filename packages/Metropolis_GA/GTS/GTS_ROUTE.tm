PiSPEC 3.0

// Copyright (C) 2022 Prover Technology, All Rights Reserved

class GTS_ROUTE {
inherit GTS_OBJECT;

Parameters[Generated]:
  ROUTE gds_inst;

// ==========================================================================
// Testcases
// ==========================================================================
TestCase:
  """ Request the route and run a train through it. """
  RUN_ROUTE
  foreach(rt:SELF.gds_inst) {
    """ Initialize the system. """
    init_system();

    """ Request all switches in the route in their proper positions. """
    foreach(sw:rt.switches_normal) {
      sw.RequestedNormal := true;
    }
    foreach(sw:rt.switches_reverse) {
      sw.RequestedReverse := true;
    }
    wait 1 SEC;
    foreach(sw:rt.objects) {
      sw.RequestedNormal := false;
      sw.RequestedReverse := false;
    }

    """ Request some protective switches in their proper positions. """
    foreach(pa:rt.protection_areas)
    if (pa.minimal) {
      foreach(sw1:pa.switches_normal) {
        sw1.RequestedNormal := true;
      }
      foreach(sw1:pa.switches_reverse) {
        sw1.RequestedReverse := true;
      }
      wait 1 SEC;
      foreach(sw1:pa.switches_normal) {
        sw1.RequestedNormal := false;
      }
      foreach(sw1:pa.switches_reverse) {
        sw1.RequestedReverse := false;
      }
    }

    """
    Assert that all switches in the route are in correspondence in proper
    positions.
    """
    expect ALL sw:rt.objects (
      (switches_normal(rt, sw) -> sw.correspondence_normal) &
      (switches_reverse(rt, sw) -> sw.correspondence_reverse)
    ) within 5 SEC;

    """
    Assert that the flank of the route is protected.
    """
    expect rt.protected_flank;

    """
    If the route does not end in a buffer stop or an exit signal, assert that
    the front of the route is protected.
    """
    expect (
      ~rt.ends_at_buffer_stop &
      ~rt.ends_at_exit_signal
    ) -> rt.protected_front;

    """ Request the route. """
    rt.RouteRequested := true;
    wait 1 SEC;
    rt.RouteRequested := false;

    """ Assert that the route is set. """
    expect rt.set;

    """ Assert that the start signal is commanded proceed and shows proceed. """
    expect ALL si:rt.start_signal (
      si.CommandedProceed & si.ShowsProceed
    );

    // Run a train through the route and assert that sectional locking
    // releases when route sections are passed over by the train.
    """ Occupy the track immediately before the route. """
    foreach(tc:rt.berth_track) {
      tc.Clear := false;
    }
    wait 1 SEC;

    """ Occupy the first track of the route. """
    foreach(tc:rt.first_track) {
      tc.Clear := false;
    }
    wait 1 SEC;

    """
    Assert that the start signal is neither commanded to proceed nor shows
    proceed.
    """
    expect ALL si:rt.start_signal (
      ~si.CommandedProceed & ~si.ShowsProceed
    );

    """ Vacate the track immediately before the route. """
    foreach(tc:rt.berth_track) {
      tc.Clear := true;
    }
    wait 1 SEC;

    """
    Traverse the rest of the route and assert that locking of route sections
    releases as the train passes over them.
    """
    foreach (ord)
    foreach (tc:rt.tracks)
    if (track_number(rt, tc) == ord.value & ~first_track(rt, tc)) {
      """ Occupy track $name(tc). """
      tc.Clear := false;
      wait 1 SEC;

      foreach(tc1)
      """ Vacate track $name(tc1). """
      if (track_number(rt, tc1) == ord.value - 1) {
        tc1.Clear := true;
      }
      wait 1 SEC;

      """
      If the track just vacated is the last track in the route section that
      contains it, assert that the locking of this route section releases.
      """
      expect ALL rts:rt.route_sections ALL tc1:rts.last_track (
        (track_number(rt, tc1) == ord.value - 1) -> ~rts.Locked
      );
    }

    """ Occupy the track immediately after the route. """
    foreach(tc:rt.track_after) {
      tc.Clear := false;
    }
    wait 1 SEC;

    """ Vacate the last track of the route. """
    foreach(tc:rt.last_track) {
      tc.Clear := true;
    }
    wait 1 SEC;

    """ Assert that the locking of the last route section is released. """
    expect ALL rts:rt.route_sections ALL tc:rt.last_track (
      tracks(rts, tc) -> ~rts.Locked
    );
  }

TestCase:
  """ 
  Test Case 3: Line block interface for exit signals. 
  """
  TEST_CASE_3
  foreach(rt:SELF.gds_inst)
  foreach(esi:rt.end_object)
  if (exit_signal(esi)) {
    
    """ 1. [Action] Initialize the system. """
    init_system();

    """ 2. [Action] Request every switch in the route in its proper position. """
    foreach(sw:rt.switches_normal) {
      sw.RequestedNormal := true;
    }
    foreach(sw:rt.switches_reverse) {
      sw.RequestedReverse := true;
    }
    wait 1 SEC;
    foreach(sw:rt.objects) {
      sw.RequestedNormal := false;
      sw.RequestedReverse := false;
    }

    """ 3. [Action] Request a sufficient set of protective switches (which might be empty) in their protective positions. """
    foreach(pa:rt.protection_areas)
    if (pa.minimal) {
      foreach(sw1:pa.switches_normal) {
        sw1.RequestedNormal := true;
      }
      foreach(sw1:pa.switches_reverse) {
        sw1.RequestedReverse := true;
      }
      wait 1 SEC;
      foreach(sw1:pa.switches_normal) {
        sw1.RequestedNormal := false;
      }
      foreach(sw1:pa.switches_reverse) {
        sw1.RequestedReverse := false;
      }
    }

    """ 4. [Expect] All switches in the route are in proper correspondence. """
    expect ALL sw:rt.objects (
      (switches_normal(rt, sw) -> sw.correspondence_normal) &
      (switches_reverse(rt, sw) -> sw.correspondence_reverse)
    ) within 5 SEC;

    """ 5. [Expect] The flank of the route is protected. """
    expect rt.protected_flank;

    """ 6. [Action] Set the line input of the exit signal $name(esi) to false """
    esi.LineInput := false;

    """ 7. [Expect] The line output of the exit signal is true during 5s """
    expect esi.LineOutput during 5 SEC;

    """ 8. [Action] Request the route. """
    rt.RouteRequested := true;
    wait 1 SEC;
    rt.RouteRequested := false;

    """ 9. [Expect] No section of the route becomes locked during 30s """
    expect (ALL rts:rt.route_sections ~rts.Locked) during 30 SEC;

    """ 10. [Action] Set the line input of the exit signal to true """
    esi.LineInput := true;

    """ 11. [Action] Request the route. """
    rt.RouteRequested := true;
    wait 1 SEC;
    rt.RouteRequested := false;

    """ 12. [Expect] The route becomes locked within 5s """
    expect rt.set within 5 SEC;

    """ 13. [Expect] The start signal of the route shows proceed within 1s """
    expect ALL si:rt.start_signal (
      si.ShowsProceed
    ) within 1 SEC;

    """ 14. [Expect] The line output of the exit signal is false during 5s """
    expect ~esi.LineOutput during 5 SEC;

    """ 15. [Action] Request manual release of the route. """
    rt.ReleaseRequested := true;
    wait 1 SEC;
    rt.ReleaseRequested := false;
    wait 35 SEC;

    """ 16. [Expect] All route sections of the route are unlocked. """
    expect ALL rts:rt.route_sections ~rts.Locked;

  }

TestCase:
  """
  Test Case 4: Manual release. The purpose of this test is to test 
  that a manual release request removes the proceed command at once
  and releases all route sections simultaneously after the 30 s delay.
  """
  TEST_CASE_4
  foreach(rt:SELF.gds_inst) {

    """ 1. [Action] Initialize the system. """
    init_system();

    """ 2. [Action] Request every switch in the route in its proper position. """
    foreach(sw:rt.switches_normal) {
      sw.RequestedNormal := true;
    }
    foreach(sw:rt.switches_reverse) {
      sw.RequestedReverse := true;
    }
    wait 1 SEC;
    foreach(sw:rt.objects) {
      sw.RequestedNormal := false;
      sw.RequestedReverse := false;
    }

    """ 3. [Action] Request a sufficient set of protective switches (which might be empty) in their protective positions. """
    foreach(pa:rt.protection_areas)
    if (pa.minimal) {
      foreach(sw1:pa.switches_normal) {
        sw1.RequestedNormal := true;
      }
      foreach(sw1:pa.switches_reverse) {
        sw1.RequestedReverse := true;
      }
      wait 1 SEC;
      foreach(sw1:pa.switches_normal) {
        sw1.RequestedNormal := false;
      }
      foreach(sw1:pa.switches_reverse) {
        sw1.RequestedReverse := false;
      }
    }

    """ 4. [Action] If the route ends in an exit signal, set the line input of the exit signal to true. """
    foreach(esi:rt.end_object)
    if (exit_signal(esi)) {
      esi.LineInput := true;
    }

    """ 5. [Expect] All switches in the route are in proper correspondence. """
    expect ALL sw:rt.objects (
      (switches_normal(rt, sw) -> sw.correspondence_normal) &
      (switches_reverse(rt, sw) -> sw.correspondence_reverse)
    ) within 5 SEC;

    """ 6. [Expect] The flank of the route is protected. """
    expect rt.protected_flank;

    """
    7. [Expect] If the route does not end in a buffer stop or an exit signal,
    the front of the route is protected.
    """
    expect (
      ~rt.ends_at_buffer_stop &
      ~rt.ends_at_exit_signal
    ) -> rt.protected_front;

    """ 8. [Action] Request the route. """
    rt.RouteRequested := true;
    wait 1 SEC;
    rt.RouteRequested := false;

    """ 9. [Expect] The route is set. """
    expect rt.set;

    """ 10. [Expect] The start signal is commanded to proceed and shows proceed. """
    expect ALL si:rt.start_signal (
      si.CommandedProceed & si.ShowsProceed
    );

    """ 11. [Action] Request release of the route. """
    rt.ReleaseRequested := true;
    wait 1 SEC;
    rt.ReleaseRequested := false;

    """
    12. [Expect] The start signal is neither commanded to proceed nor shows
    proceed.
    """
    expect ALL si:rt.start_signal (
      ~si.CommandedProceed & ~si.ShowsProceed
    );

    """ 13. [Expect] The route is not set. """
    expect ~rt.set;

    """
    14. [Expect] During the following 28 s, all route sections stay locked
    and the start signal is not commanded to proceed.
    """
    expect (
      (ALL rts:rt.route_sections rts.Locked) &
      (ALL si:rt.start_signal ~si.CommandedProceed)
    ) during 28 SEC;

    """
    15. [Expect] During the following 4 s, the route sections are either all
    locked or all unlocked at every instant, i.e. they release simultaneously.
    """
    expect ALL rts1:rt.route_sections ALL rts2:rt.route_sections (
      ((rts1.Locked & rts2.Locked) # (~rts1.Locked & ~rts2.Locked)) &
      (ALL si:rt.start_signal ~si.CommandedProceed)
    ) during 4 SEC;

    """ 16. [Expect] All route sections of the route are unlocked. """
    expect ALL rts:rt.route_sections (
      ~rts.Locked
    );
  }
}