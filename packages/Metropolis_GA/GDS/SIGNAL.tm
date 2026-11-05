PiSPEC 3.0

class GDS_SIGNAL {
inherit SIGNAL;

Equations:

  CommandedProceed :=
  ~exit_signal(SELF) &
  SOME rt (
    start_signal(rt, SELF) &
    ready_to_proceed(rt)
  );

}
