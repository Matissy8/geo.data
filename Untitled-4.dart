// lib/core/scoring/scoring.dart
int clampInt(int v, int min, int max) => v < min ? min : (v > max ? max : v);

double clampDouble(double v, double min, double max) =>
    v < min ? min : (v > max ? max : v);

class ScoreInput {
  ScoreInput({
    required this.taskBasePoints,
    required this.taskCorrectness, // 0..1
    required this.taskDurationSec,
    required this.taskTimeLimitSec,
  });

  final int taskBasePoints;
  final double taskCorrectness;
  final int taskDurationSec;
  final int taskTimeLimitSec;
}

int calcTaskPoints(ScoreInput s) {
  final ratio = s.taskTimeLimitSec <= 0 ? 1.0 : (s.taskDurationSec / s.taskTimeLimitSec);
  final timeFactor = clampDouble(1.15 - ratio * 0.35, 0.8, 1.15);
  final pts = s.taskBasePoints * s.taskCorrectness * timeFactor;
  return pts.round();
}

int calcSkipPenalty({
  required int skippedCount,
  required int skipPenaltyPoints, // e.g. 150
}) {
  final penalizedSkips = (skippedCount - 2);
  if (penalizedSkips <= 0) return 0;
  return penalizedSkips * skipPenaltyPoints;
}

int calcSpeedScore({
  required int completedCheckpoints,
  required int totalCheckpoints,
  required int bestPossibleTimeSec, // e.g. 35min=2100
  required int teamTimeSec,
  required int speedBase, // e.g. 800
}) {
  if (totalCheckpoints <= 0) return 0;
  final completionRate = completedCheckpoints / totalCheckpoints;
  if (completionRate < 0.70) return 0;

  final speedRatio = bestPossibleTimeSec <= 0 ? 0.0 : (bestPossibleTimeSec / teamTimeSec);
  final clamped = clampDouble(speedRatio, 0.2, 1.2);
  return (speedBase * clamped).round();
}

class ScoreBreakdown {
  ScoreBreakdown({
    required this.taskScore,
    required this.speedScore,
    required this.skipPenalty,
    required this.totalScore,
  });

  final int taskScore;
  final int speedScore;
  final int skipPenalty;
  final int totalScore;
}
