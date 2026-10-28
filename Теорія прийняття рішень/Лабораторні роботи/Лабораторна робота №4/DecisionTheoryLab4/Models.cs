namespace DecisionTheoryLab4;

public sealed record PairwiseResult(
    string Name,
    IReadOnlyList<double> Priorities,
    double LambdaMax,
    double ConsistencyIndex,
    double ConsistencyRatio)
{
    public bool IsConsistent => ConsistencyRatio < 0.1;
}

public sealed record ScaleAnalysis(
    string ScaleName,
    PairwiseResult Criteria,
    IReadOnlyList<PairwiseResult> AlternativesByCriterion,
    IReadOnlyList<double> GlobalPriorities,
    int BestAlternativeIndex);

public static class Variant12Data
{
    public static readonly string[] Alternatives = ["Водоканал", "Центр", "Молодіжне"];
    public static readonly string[] Criteria = ["Вартість", "Етажність", "Час поїздки до роботи"];

    public static ScaleAnalysis AnalyzeThreePointScale() => Analyze(
        "Трибальна шкала",
        criteria: Matrix(
            [1, 3, 2],
            [1.0 / 3, 1, 1.0 / 2],
            [1.0 / 2, 2, 1]),
        alternatives:
        [
            Matrix([1, 2, 1.0 / 2], [1.0 / 2, 1, 1.0 / 3], [2, 3, 1]),
            Matrix([1, 2, 3], [1.0 / 2, 1, 2], [1.0 / 3, 1.0 / 2, 1]),
            Matrix([1, 1.0 / 2, 2], [2, 1, 3], [1.0 / 2, 1.0 / 3, 1])
        ]);

    public static ScaleAnalysis AnalyzeNinePointScale() => Analyze(
        "Дев'ятибальна шкала Сааті",
        criteria: Matrix(
            [1, 5, 3],
            [1.0 / 5, 1, 1.0 / 3],
            [1.0 / 3, 3, 1]),
        alternatives:
        [
            Matrix([1, 3, 1.0 / 3], [1.0 / 3, 1, 1.0 / 5], [3, 5, 1]),
            Matrix([1, 3, 5], [1.0 / 3, 1, 3], [1.0 / 5, 1.0 / 3, 1]),
            Matrix([1, 1.0 / 3, 3], [3, 1, 5], [1.0 / 3, 1.0 / 5, 1])
        ]);

    public static double[,] GetThreePointCriteriaMatrix() => Matrix(
        [1, 3, 2], [1.0 / 3, 1, 1.0 / 2], [1.0 / 2, 2, 1]);

    public static double[,] GetNinePointCriteriaMatrix() => Matrix(
        [1, 5, 3], [1.0 / 5, 1, 1.0 / 3], [1.0 / 3, 3, 1]);

    private static ScaleAnalysis Analyze(string scaleName, double[,] criteria, double[][,] alternatives)
    {
        var criteriaResult = AhpAnalyzer.Analyze("Критерії", criteria);
        var localResults = alternatives
            .Select((matrix, index) => AhpAnalyzer.Analyze(Criteria[index], matrix))
            .ToArray();
        var global = AhpAnalyzer.Aggregate(criteriaResult.Priorities, localResults);
        return new ScaleAnalysis(
            scaleName,
            criteriaResult,
            localResults,
            global,
            Array.IndexOf(global.ToArray(), global.Max()));
    }

    private static double[,] Matrix(params double[][] rows)
    {
        var matrix = new double[rows.Length, rows.Length];
        for (var row = 0; row < rows.Length; row++)
        for (var column = 0; column < rows.Length; column++)
            matrix[row, column] = rows[row][column];
        return matrix;
    }
}
