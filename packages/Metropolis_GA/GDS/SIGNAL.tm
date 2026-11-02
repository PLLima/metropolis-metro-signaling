PiSPEC 3.0

class GDS_SIGNAL {
inherit SIGNAL;

Equations:

  CommandedProceed :=
    ~exit_signal(SELF) &
    SOME rt (
      start_signal(rt, SELF) &
      ready_to_proceed(rt)
    ) #
    exit_signal(SELF) &
    end_locked(SELF) &
    SOME tc (
      track_after(SELF, tc) &
      Clear(tc)
    );

}
