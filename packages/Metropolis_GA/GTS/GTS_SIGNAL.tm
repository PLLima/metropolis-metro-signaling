PiSPEC 3.0

// Copyright (C) 2022 Prover Technology, All Rights Reserved

class GTS_SIGNAL {
inherit GTS_OBJECT;

Parameters[Generated]:
  SIGNAL gds_inst;

Inputs:
  GreenLampFailure;

Feedbacks:
  foreach (si:SELF.gds_inst) {
    si.ShowsProceed := si.CommandedProceed & ~SELF.GreenLampFailure;
  }

}
