PiSPEC 3.0

// Copyright (C) 2022 Prover Technology, All Rights Reserved

class GVS_SIGNAL {

Parameters[Generated]:
  SIGNAL gds_inst;

Equations:

  Background := true;

  // Confirmed aspect (inputs from wayside)

  Green1 := SOME si:SELF.gds_inst si.ShowsProceed;
  Yellow1 := false;
  Red1 := false;

  Green2 := false;
  Yellow2 := false;
  Red2 := SOME si:SELF.gds_inst ~si.ShowsProceed;

  // Commanded aspect (output from IL)

  Green1Dot := SOME si:SELF.gds_inst si.CommandedProceed;
  Yellow1Dot := false;
  Red1Dot := false;

  Green2Dot := false;
  Yellow2Dot := false;
  Red2Dot := false;

}
