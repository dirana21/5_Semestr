namespace DecisionTheoryLab2;

public sealed record ExpertEvaluation(
    int ObjectId,
    IReadOnlyList<double> Scores,
    IReadOnlyList<double> Ranks);

public sealed record ObjectResult(
    int ObjectId,
    double ScoreSum,
    double ScoreWeight,
    double RankSum,
    double AverageRank,
    double MedianRank,
    double FinalAverageRank,
    double FinalMedianRank,
    double RankWeight,
    double Deviation,
    double SquaredDeviation);

public sealed record AnalysisResult(
    IReadOnlyList<ObjectResult> Objects,
    double MeanRankSum,
    double SquaredDeviationSum,
    double Concordance,
    bool IsConcordant);
