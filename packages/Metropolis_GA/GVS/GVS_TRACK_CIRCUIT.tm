PiSPEC 3.0

// Copyright (C) 2014 Prover Technology, All Rights Reserved

class GVS_TRACK_CIRCUIT {

Parameters[Generated]:
  TRACK_CIRCUIT gds_inst;

Equations:

  Occupied := SOME tc:SELF.gds_inst ~tc.Clear;

}
