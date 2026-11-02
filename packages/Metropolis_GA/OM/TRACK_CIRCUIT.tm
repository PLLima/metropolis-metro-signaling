PiSPEC 3.0

abstract class TRACK_CIRCUIT {
inherit AREA;

Variables:
  tc, tc1;

Inputs:

  """
  Input from the wayside. The track is clear of occupancy.
  """
  Clear;

Functions:

  """
  Two track circuits are adjacent if they, regarded as areas, share nodes but
  not edges.
  """
  bool adjacent(TRACK_CIRCUIT tc) :=
   intersects_by_node(SELF, tc) &
  ~intersects_by_edge(SELF, tc);

  """
  A track circuit is an exit track if it has precisely one adjacent track
  circuit and is behind an exit signal. Such tracks represents lines leading
  off to other stations.
  """
  bool exit_track :=
    SOME tc:SELF.adjacent (
      ALL tc1:SELF.adjacent (
        tc1=tc
      )
    ) &
    SOME esi (
      track_after(esi, SELF)
    );

Attributes:

  InteractiveDefault: Clear["True"];

  NormalValue: Clear["True"];

}
