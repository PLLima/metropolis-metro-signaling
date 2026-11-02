PiSPEC 3.0

// Copyright (C) 2014 Prover Technology, All Rights Reserved

class GVS_SWITCH {

Parameters[Generated]:
  SWITCH gds_inst;

Equations:

  Background := true;

  // Detection
  DetectedNormal := SOME sw:SELF.gds_inst sw.DetectedNormal;
  DetectedReverse := SOME sw:SELF.gds_inst sw.DetectedReverse;

  // Command (state in interlocking)
  CommandedNormal := SOME sw:SELF.gds_inst sw.CommandedNormal;
  CommandedReverse := SOME sw:SELF.gds_inst sw.CommandedReverse;

  // Move output to switch
  MoveNormal := SOME sw:SELF.gds_inst sw.MoveNormal;
  MoveReverse := SOME sw:SELF.gds_inst sw.MoveReverse;

Attributes:

  VisualizationEffect : MoveNormal["Blink"];
  VisualizationEffect : MoveReverse["Blink"];

}
