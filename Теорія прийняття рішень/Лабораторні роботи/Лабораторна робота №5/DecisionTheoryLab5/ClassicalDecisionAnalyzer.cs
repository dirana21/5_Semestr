namespace DecisionTheoryLab5;

public static class ClassicalDecisionAnalyzer
{
    private const double Tolerance = 1e-9;

    public static DecisionAnalysis Analyze(double[,] matrix, IReadOnlyList<double> probabilities)
    {
        Validate(matrix, probabilities);
        var rows = matrix.GetLength(0);
        var columns = matrix.GetLength(1);

        var rowMinimums = Enumerable.Range(0, rows)
            .Select(i => Enumerable.Range(0, columns).Min(j => matrix[i, j]))
            .ToArray();

        var expectations = Enumerable.Range(0, rows)
            .Select(i => Enumerable.Range(0, columns).Sum(j => matrix[i, j] * probabilities[j]))
            .ToArray();

        var columnMaxima = Enumerable.Range(0, columns)
            .Select(j => Enumerable.Range(0, rows).Max(i => matrix[i, j]))
            .ToArray();

        var regrets = new double[rows, columns];
        for (var i = 0; i < rows; i++)
        for (var j = 0; j < columns; j++)
            regrets[i, j] = columnMaxima[j] - matrix[i, j];

        var maximumRegrets = Enumerable.Range(0, rows)
            .Select(i => Enumerable.Range(0, columns).Max(j => regrets[i, j]))
            .ToArray();

        return new DecisionAnalysis(
            CreateMaximumResult("Мінімаксний критерій", rowMinimums),
            CreateMaximumResult("Критерій Байєса-Лапласа", expectations),
            CreateMinimumResult("Критерій Севіджа", maximumRegrets),
            regrets,
            columnMaxima);
    }

    private static CriterionResult CreateMaximumResult(string name, double[] scores)
    {
        var best = scores.Max();
        return new CriterionResult(name, scores, Winners(scores, best), true);
    }

    private static CriterionResult CreateMinimumResult(string name, double[] scores)
    {
        var best = scores.Min();
        return new CriterionResult(name, scores, Winners(scores, best), false);
    }

    private static int[] Winners(IReadOnlyList<double> values, double target) =>
        values.Select((value, index) => (value, index))
            .Where(item => Math.Abs(item.value - target) <= Tolerance)
            .Select(item => item.index + 1)
            .ToArray();

    private static void Validate(double[,] matrix, IReadOnlyList<double> probabilities)
    {
        if (matrix.GetLength(0) == 0 || matrix.GetLength(1) == 0)
            throw new ArgumentException("Матриця не може бути порожньою.", nameof(matrix));
        if (matrix.GetLength(1) != probabilities.Count)
            throw new ArgumentException("Кількість імовірностей має відповідати кількості станів.", nameof(probabilities));
        if (probabilities.Any(p => p < 0))
            throw new ArgumentException("Імовірності не можуть бути від'ємними.", nameof(probabilities));
        if (Math.Abs(probabilities.Sum() - 1.0) > Tolerance)
            throw new ArgumentException("Сума імовірностей має дорівнювати 1.", nameof(probabilities));
    }
}
