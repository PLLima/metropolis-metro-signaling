PiSPEC 3.0

abstract class PROTECTION_AREA {
inherit AREA;

Variables:
  pa, pa1;

Parameters:

  """
  Underlying protection paths.
  """
  set<PROTECTION_PATH> paths;

Functions:

  """
  Signal protected by the protection area.
  """
  bool protects_signal(SIGNAL si) :=
    ALL ppt:SELF.paths start_object(ppt, si);

  """
  Switch in normal position that is protected by the protection area.
  """
  bool protects_sw_normal(SWITCH sw) :=
    ALL ppt:SELF.paths (
      start_object(ppt, sw) &
      switches_reverse(ppt, sw)
    );

  """
  Switch in reverse position that is protected by the protection area.
  """
  bool protects_sw_reverse(SWITCH sw) :=
    ALL ppt:SELF.paths (
      start_object(ppt, sw) &
      switches_normal(ppt, sw)
    );

  """
  Object that is protected by the protection area.
  """
  bool protects_object(PROTECTED_OBJECT prt_obj) :=
    ALL ppt:SELF.paths (
      start_object(ppt, prt_obj)
    );

  """
  Tracks required clear for the protection area to be protective.
  """
  bool tracks_clear(TRACK_CIRCUIT tc) :=
    SOME ppt:SELF.paths (
      tracks(ppt, tc) &
      ~SOME sw:tc.objects (
        switches_normal(SELF, sw) #
        switches_reverse(SELF, sw)
      )
    );

  """
  Switches required in normal position for the protection area to be protective.
  """
  bool switches_normal(SWITCH sw) :=
    SOME ppt:SELF.paths (
      end_object(ppt, sw) &
      switches_reverse(ppt, sw)
    );

  """
  Switches required in reverse position for the protection area to be
  protective.
  """
  bool switches_reverse(SWITCH sw) :=
    SOME ppt:SELF.paths (
      end_object(ppt, sw) &
      switches_normal(ppt, sw)
    );

  """
  The protection area is minimal, i.e. it is contained in all protection areas
  with the same origin.
  """
  bool minimal :=
    ALL pa
    SOME prt_obj:SELF.protects_object (
      protects_object(pa, prt_obj) ->
        ALL ppt:SELF.paths (
          SOME ppt1:pa.paths (
            subpath(ppt, ppt1)
          )
        )
    );

Functions:

  """
  The protection area is protective, i.e. all tracks that are required clear
  are clear and all required switches are detected in correct positions.
  """
  bool protective :=
    ALL tc:SELF.tracks_clear tc.Clear &
    ALL sw:SELF.switches_normal sw.correspondence_normal &
    ALL sw:SELF.switches_reverse sw.correspondence_reverse;

}
