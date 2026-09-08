namespace DecisionTheoryLab1;

public sealed record Alternative(int Id, double Performance, double Cost, double Efficiency);

public sealed record Evaluation(
    Alternative Alternative,
    double WeightedPerformance,
    double WeightedCost,
    double WeightedEfficiency,
    double NormalizedPerformance,
    double NormalizedCost,
    double NormalizedEfficiency,
    double Utility);
