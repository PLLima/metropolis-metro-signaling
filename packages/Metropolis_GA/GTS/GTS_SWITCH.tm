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

}
