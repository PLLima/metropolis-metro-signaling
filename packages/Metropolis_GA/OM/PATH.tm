PiSPEC 3.0

abstract class PATH {

Variables:
  pt, pt1;

Parameters:

  """
  Intersecting paths.
  """
  set<PATH> intersects;

  """
  Intersecting paths with at least one edge in the opposite direction.
  """
  set<PATH> opposes;

  """
  Paths that follow immediately after this one (same node and same direction).
  """
  set<PATH> follows;

  """
  Subpaths of this path.
  """
  set<PATH> subpath;

  """
  Tracks in the path.
  """
  set<TRACK_CIRCUIT> tracks;

  """
  Objects in the path.
  """
  set<OBJECT> objects;

  """
  Objects that are facing in the path.
  """
  set<OBJECT> facing;

  """
  Objects that are trailing in the path.
  """
  set<OBJECT> trailing;

  """
  Switches that are normal in the path.
  """
  set<SWITCH> switches_normal;

  """
  Switches that are reverse in the path.
  """
  set<SWITCH> switches_reverse;

  """
  Zero-based index for track circuits in the path.
  """
  int track_number(TRACK_CIRCUIT);

Functions:

  """
  The length of the path.
  """
  int length := SUM tc:SELF.tracks 1;

  """
  The first track of the path.
  """
  bool first_track(TRACK_CIRCUIT tc) :=
    track_number(SELF, tc) == 0;

  """
  The last track of the path.
  """
  bool last_track(TRACK_CIRCUIT tc) :=
    track_number(SELF, tc) == SELF.length - 1;

  """
  Paths leading up to this one.
  """
  bool precedes(PATH pt) :=
    follows(pt, SELF);

}
