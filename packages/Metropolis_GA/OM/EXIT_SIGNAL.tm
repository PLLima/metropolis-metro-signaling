PiSPEC 3.0

abstract class EXIT_SIGNAL {
inherit SIGNAL;

Variables:
  esi, esi1;

Inputs:

  """
  Input from neighbouring station indicating that the exit signal at the
  other end of the line is at stop and not end locked.
  """
  LineInput;

Equations:

  """
  Output to neighbouring station indicating that this exit signal is at stop
  and not end locked.
  """
  LineOutput;

Outputs:

  LineOutput;

Attributes:

  SimulatorInitialValue: LineInput["True"];

}
