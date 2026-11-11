namespace DecisionTheoryLab7;

public sealed record DominanceStep(
    string RemovedStrategy,
    string DominatingStrategy,
    string Explanation);

public sealed record PureStrategyAnalysis(
    IReadOnlyList<double> RowMinimums,
    IReadOnlyList<double> ColumnMaximums,
    double LowerValue,
    double UpperValue,
    IReadOnlyList<(int Row, int Column)> SaddlePoints);

public sealed record MatrixGameAnalysis(
    double[,] OriginalMatrix,
    double[,] ReducedMatrix,
    IReadOnlyList<int> ActiveRows,
    IReadOnlyList<int> ActiveColumns,
    IReadOnlyList<DominanceStep> ReductionSteps,
    PureStrategyAnalysis OriginalPureAnalysis,
    PureStrategyAnalysis ReducedPureAnalysis,
    IReadOnlyList<double> RowProbabilities,
    IReadOnlyList<double> ColumnProbabilities,
    double GameValue,
    IReadOnlyList<double> PayoffAgainstColumns,
    IReadOnlyList<double> PayoffForRows);

public static class Variant12Data
{
    public static double[,] Matrix => new[,]
    {
        { -2.0, -5.0, -4.0,  0.0 },
        {  4.0,  3.0,  0.0, -3.0 },
        {  1.0,  0.0, -3.0,  4.0 },
        { -3.0, -5.0,  3.0,  5.0 }
    };
}
