erDiagram
  USER ||--o{ TEAMMEMBER : has
  TEAM ||--o{ TEAMMEMBER : includes
  RACE_EVENT ||--o{ CHECKPOINT : has
  CHECKPOINT ||--o{ TASK : contains
  TEAM ||--o{ TEAM_RACE_RUN : participates
  RACE_EVENT ||--o{ TEAM_RACE_RUN : includes
  TEAM_RACE_RUN ||--o{ CHECKPOINT_VISIT : visits
  TEAM_RACE_RUN ||--o{ TASK_ATTEMPT : attempts
  TEAM_RACE_RUN ||--o{ LOCATION_PING : pings
  TEAM_RACE_RUN ||--|| SCORE_BREAKDOWN : results

  USER {
    string id
    string email
    string displayName
    string role  "player/admin"
    datetime createdAt
  }

  TEAM {
    string id
    string name
    string school
    string classLabel "9.A"
    string createdByUserId
    datetime createdAt
  }

  TEAMMEMBER {
    string id
    string teamId
    string firstName
    string lastName
    datetime addedAt
  }

  RACE_EVENT {
    string id
    string title
    datetime startAt
    datetime endAt
    int totalTimeLimitSec
    int bestPossibleTimeSec
    int speedBase
    int skipPenaltyPoints
    string status "draft/live/ended"
  }

  CHECKPOINT {
    string id
    string raceEventId
    int orderIndex
    string title
    double lat
    double lng
    int radiusM
    string qrToken
    string pinCode
    boolean isFinish
  }

  TASK {
    string id
    string checkpointId
    string type "mcq/multi/short"
    string prompt
    int basePoints
    int timeLimitSec
    string correctAnswerJson
  }

  TEAM_RACE_RUN {
    string id
    string teamId
    string raceEventId
    datetime startedAt
    datetime endedAt
    string status "not_started/running/finished/time_up"
    int currentCheckpointIndex
    int completedCount
    int skippedCount
  }

  CHECKPOINT_VISIT {
    string id
    string teamRaceRunId
    string checkpointId
    string status "completed/skipped"
    datetime at
  }

  TASK_ATTEMPT {
    string id
    string teamRaceRunId
    string taskId
    datetime openedAt
    datetime submittedAt
    int durationSec
    double correctness "0..1"
    string answerJson
  }

  LOCATION_PING {
    string id
    string teamRaceRunId
    double lat
    double lng
    double accuracyM
    datetime at
  }

  SCORE_BREAKDOWN {
    string id
    string teamRaceRunId
    int taskScore
    int speedScore
    int skipPenalty
    int totalScore
    double correctPercent
    int totalTimeSec
  }
