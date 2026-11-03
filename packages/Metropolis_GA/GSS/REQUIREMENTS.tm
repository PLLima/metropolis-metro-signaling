PiSPEC 3.0

class REQUIREMENTS {

StaticInstances:
  requirements;

Inputs:

  InitialCycle;

Functions:

  bool initial_cycle :=
    SELF.InitialCycle;

Attributes:

  SpecialVariable: InitialCycle["Init"];

Prove:

  """
  If a signal is commanded to proceed, then one of the following holds:
  1. It is not an exit signal and there is a unique set route that
     starts at the signal.
  2. It is an exit signal, it is end locked and the track circuit behind it
     is clear of occupancy.
  """
  GSS_01_1 :=
    ALL si (
      ~exit_signal(si) &
      CommandedProceed(si) ->
        SOME rt (
          start_signal(rt, si) &
          set(rt) &
          ALL rt1 (
            start_signal(rt1, si) &
            set(rt1) ->
              rt1 = rt
          )
        )
    );

  GSS_01_2 :=
    ALL si (
      exit_signal(si) &
      CommandedProceed(si) ->
        end_locked(si) &
        SOME tc (
          track_after(si, tc) &
          Clear(tc)
        )
    );

  """
  Route sections which share tracks cannot be locked at the same
  time.
  """
  
  GSS_02 :=
    ALL rts1
    ALL rts2(
      (~(rts1=rts2) &
      SOME tc(
       tracks(rts1,tc) & tracks(rts2,tc))  -> 
        ~(rts1.Locked & rts2.Locked)));


  """
  If a signal that is the start of a set route is commanded to proceed, then
  the switches in the route are detected in their correct positions.

  The switchess in the route are given by the relations Switch In
  Normal/Reverse relations from the route sections in the route.
  """

  GSS_03 :=
    ALL si
    ALL rt
    ALL rts (
      CommandedProceed(si) &
      start_signal(rt, si) &
      set(rt) &
      route_sections(rt, rts) ->
        ALL sw (
          (switches_normal(rts, sw) ->
             DetectedNormal(sw)) &
          (switches_reverse(rts, sw) ->
             DetectedReverse(sw))
        )
    );


  """
  If a signal that is the start of a set route is commanded to proceed, then
  all tracks in the route are clear from occupancy.

  The tracks in the route are given by the tracks in the route sections in the
  route.
  """
  GSS_04 :=
    ALL si
    ALL rt
    ALL rts (
      CommandedProceed(si) &
      start_signal(rt, si) &
      set(rt) &
      route_sections(rt, rts) ->
        ALL tc (
          tracks(rts, tc) ->
            Clear(tc)
        )
    );

  """
  If a signal that is the start of a set route is commanded to proceed, then,
  for every switch in the route, there is a protection area that is protective
  (flank protection).
  """
  GSS_05 :=
    ALL si
    ALL rt
    ALL rts (
      CommandedProceed(si) &
      start_signal(rt, si) &
      set(rt) &
      route_sections(rt, rts) ->
        ALL sw (
          (switches_normal(rts, sw) ->
             SOME pa (
               protects_sw_normal(pa, sw) &
               protective(pa)
             )) &
             (switches_reverse(rts, sw) ->
                SOME pa (
                  protects_sw_reverse(pa, sw) &
                  protective(pa)
                ))
        )
    );

  """
  If a signal that is the start of a set route is commanded to
  proceed, then either the route ends at a buffer stop, ends at an
  exit signal, the end signal is commanded to proceed, or there is
  a protective area for the end signal that is protective (front
  protection)
  """
  GSS_06 :=
    ALL si
    ALL rt (
      CommandedProceed(si) &
      start_signal(rt, si) &
      set(rt) ->
        SOME bs:rt.end_object true #
        SOME esi:rt.end_object true #
        SOME si1:rt.end_object (
          CommandedProceed(si1) # PRE CommandedProceed(si1) #
          SOME pa (
            protects_signal(pa, si1) &
            protective(pa)
          )
        )
    );

  """
  A switch cannot be moved if any of the following holds:
    1. The switch is located in a locked route section.
    2. The switch is a protective object to another switch that is located
       in a locked route section.
    3. The switch is a protective object to an end locked signal that is not
       commanded to proceed.
  """
  GSS_07 :=
    ALL sw (
      SOME rts (
        Locked(rts) & (
          // Case 1
          switches_normal(rts, sw) #
          switches_reverse(rts, sw) #
          // Case 2
          SOME pa
          SOME sw1 (
            protective(pa) & (
              switches_normal(pa, sw) #
              switches_reverse(pa, sw)
            ) & (
              switches_normal(rts, sw1) &
              protects_sw_normal(pa, sw1) #
              switches_reverse(rts, sw1) &
              protects_sw_reverse(pa, sw1)
            )
          )
        )
      ) #
      // Case 3
      SOME pa
      SOME si (
        protects_signal(pa, si) & (
          switches_normal(pa, sw) #
          switches_reverse(pa, sw)
        ) &
        protective(pa) &
        end_locked(si) &
        ~CommandedProceed(si)
      ) ->
        ~MoveNormal(sw) &
        ~MoveReverse(sw)
    );

    """
  If a route section becomes ready to release, then it's occupied.
  """
  GSS_08 :=
    ALL rts (
      rts.ReadyToRelease & PRE ~rts.ReadyToRelease -> 
        ALL tc (
          tracks(rts, tc) ->
          ~tc.Clear
        )
    );
  
  """
  If a route section is ready to release, then it is locked
  """
 GSS_09 :=
    ALL rts (
      ReadyToRelease(rts) ->
        PRE Locked(rts)
    );

  """
  The track after an exit signal shall always be an exit track.
  """
  DATACHECK_01 :=
    ALL si (
      exit_signal(si) ->
        SOME tc (
          track_after(si, tc) &
          exit_track(tc)
        )
    );

  """
  Exit signal must always be placed back-to-back with a normal signal.
  """
  DATACHECK_02 :=
    ALL esi (
      SOME tc:esi.track_after (
        SOME si (
          ~EXIT_SIGNAL(si) &
          track_before(si, tc)
        )
      )
    );

  """
  There are no switches in exit tracks.
  """
  DATACHECK_03 :=
    ALL tc (
      exit_track(tc) ->
        ~SOME sw (
          track(sw, tc)
        )
    );

}
