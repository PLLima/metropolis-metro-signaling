PiSPEC 3.0

// Copyright (C) 2022 Prover Technology, All Rights Reserved

class GTS_SWITCH {
inherit GTS_OBJECT;

Parameters[Generated]:
  SWITCH gds_inst;

Inputs:
  """
  Simulating failed motor. The switch will not move.
  """
  MotorFailure;

  """
  Simulating failed normal detection. The switch detection does not work.
  """
  NormalDetectionFailure;

  """
  Simulating failed reverse detection. The switch detection does not work.
  """
  ReverseDetectionFailure;

Equations:

  """
  The switch is moving to the normal position.
  """
  MoveNormal :=
    SOME sw:SELF.gds_inst(
      sw.MoveNormal &
      ~SELF.MotorFailure
    );

  """
  The switch is moving to the reverse position.
  """
  MoveReverse :=
    SOME sw:SELF.gds_inst (
      sw.MoveReverse &
      ~SELF.MotorFailure
    );

  """
  The switch has been moving to the normal position for three seconds.
  """
  MovementNormalComplete := SELF.MoveNormal;

  """
  The switch has been moving to the reverse position for three seconds.
  """
  MovementReverseComplete := SELF.MoveReverse;

  """
  The switch is physically in the normal position.
  """
  PhysicallyNormal :=
    ~SELF.MoveReverse &
    (SELF.MovementNormalComplete #
     SELF.DetectedNormal #
     SELF.PhysicallyNormal);

  """
  The switch is physically in the reverse position.
  """
  PhysicallyReverse :=
    ~SELF.MoveNormal &
    (SELF.MovementReverseComplete #
     SELF.DetectedReverse #
     SELF.PhysicallyReverse);

  """
  The switch is detected in the normal position.
  """
  DetectedNormal :=
    SELF.PhysicallyNormal &
    ~SELF.NormalDetectionFailure;

  """
  The switch is detected in the reverse position.
  """
  DetectedReverse :=
    SELF.PhysicallyReverse &
    ~SELF.ReverseDetectionFailure;

Feedbacks:
  foreach (sw:SELF.gds_inst) {
    sw.DetectedNormal := SELF.DetectedNormal;
    sw.DetectedReverse := SELF.DetectedReverse;
  }

Attributes:

  SimulatorInitialValue: PhysicallyNormal["True"];

Timers:
  MovementNormalComplete  (SET = 3 SEC, CLEAR = 0 SEC, FIXED);
  MovementReverseComplete (SET = 3 SEC, CLEAR = 0 SEC, FIXED);

// ==========================================================================
// Testcases
// ==========================================================================
TestCase:
  """ 
  Test Case 2: The purpose of this test is to test manual switch throwing and 
  that the switch cannot be moved when the track circuit of the switch is occupied 
  """
  MANUAL_SWITCH_THROWING
  foreach(sw:SELF.gds_inst) {
    """ Initialize the system. """
    init_system();

    """ 1. [Action] Request the switch to reverse position """
    sw.RequestedReverse := true;
    sw.RequestedNormal := false;

    """ 2. [Expect] The switch loses normal detection within 1s """
    expect ~sw.DetectedNormal within 1 SEC;

    """ 3. [Expect] The switch gains reverse detection within 4s """
    // the simulated switch needs 3 s to move so 4s is needed.
    // The test assumes the switch starts in normal position.
    expect sw.DetectedReverse within 4 SEC;

    """ 4. [Action] Request the switch to normal position """
    sw.RequestedNormal := true;
    sw.RequestedReverse := false;

    """ 5. [Expect] The switch loses reverse detection within 1s """
    expect ~sw.DetectedReverse within 1 SEC;

    """ 6. [Expect] The switch gains normal detection within 4s """
    expect sw.DetectedNormal within 4 SEC;

    """ 7. [Action] Occupy the track circuit that contains the switch """
    foreach(tc:sw.track) {
      tc.Clear := false;
    }
    wait 1 SEC;

    """ 8. [Action] Request the switch to reverse position """
    sw.RequestedReverse := true;
    sw.RequestedNormal := false;

    """ 9. [Expect] The switch stays in normal position during 60s """
    expect sw.DetectedNormal during 60 SEC;
    sw.RequestedReverse := false;
  }
}
