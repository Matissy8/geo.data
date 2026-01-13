DateTime? openedAt;

void onTaskOpened() {
  openedAt = DateTime.now();
}

Map<String, dynamic> onSubmitTask({
  required String answerJson,
  required double correctness,
}) {
  final submittedAt = DateTime.now();
  final durationSec = openedAt == null ? 0 : submittedAt.difference(openedAt!).inSeconds;

  return {
    "openedAt": openedAt?.toIso8601String(),
    "submittedAt": submittedAt.toIso8601String(),
    "durationSec": durationSec,
    "correctness": correctness,
    "answerJson": answerJson,
  };
}
