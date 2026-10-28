namespace DecisionTheoryLab5;

public sealed record CriterionResult(
    string Name,
    IReadOnlyList<double> Scores,
    IReadOnlyList<int> OptimalAlternatives,
    bool IsMaximumCriterion);

public sealed record DecisionAnalysis(
    CriterionResult Minimax,
    CriterionResult BayesLaplace,
    CriterionResult Savage,
    double[,] RegretMatrix,
    IReadOnlyList<double> ColumnMaxima);

public static class Variant12Data
{
    public static double[,] Matrix => new[,]
    {
        { -0.700, -0.500, -0.210, -0.086, -0.702, -0.500, -0.020, -0.770 },
        { -0.500, -0.400, -0.060, -0.010, -0.605, -0.930, -0.100, -0.560 },
        { -0.030, -0.600, -0.500, -0.260, -0.180, -0.930, -0.770, -0.530 },
        { -0.260, -0.010, -0.310, -0.500, -0.583, -0.600, -0.640, -0.180 },
        { -0.170, -0.160, -0.500, -0.960, -0.390, -0.870, -0.150, -0.550 },
        { -0.750, -0.500, -0.220, -0.030, -0.250, -0.730, -0.690, -0.105 },
        { -0.920, -0.180, -0.650, -0.200, -0.390, -0.060, -0.940, -0.460 },
        { -0.750, -0.700, -0.260, -0.950, -0.010, -0.820, -0.520, -0.010 }
    };

    public static double[] Probabilities => new[] { 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1 };
}
