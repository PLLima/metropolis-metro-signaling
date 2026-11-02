PiSPEC 3.0

// Copyright (C) 2022 Prover Technology, All Rights Reserved

class GTS_OBJECT {

Procedures:

  // ---------------------------------------------
  // Initialization
  // ---------------------------------------------
  """
  Initialize system.
  """
  init_system() {

    """
    Set all tracks clear.
    """
    foreach(tc) {
      tc.Clear := true;
    }

  }
}
