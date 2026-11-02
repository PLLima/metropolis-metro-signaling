PiSPEC 3.0

// Copyright (C) 2014 Prover Technology, All Rights Reserved

class GVS_ROUTE_SECTION {

Parameters[Generated]:
  ROUTE_SECTION gds_inst;

Equations:

  Requested :=
    SOME rts:SELF.gds_inst
    SOME rt (
      route_sections(rt, rts) &
      rt.RouteRequested
    );

  Locked := SOME rts:SELF.gds_inst rts.Locked;

Attributes:

  VisualizationOffsetY : Locked["2"];

}
