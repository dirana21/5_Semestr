namespace DecisionTheoryLab6;

public static class DerivedDecisionAnalyzer
{
    private const double Tolerance = 1e-9;

    public static DerivedDecisionAnalysis Analyze(
        double[,] matrix,
        IReadOnlyList<double> probabilities,
        double hurwiczCoefficient,
        double confidenceCoefficient,
        double positiveOffset)
    {
        Validate(matrix, probabilities, hurwiczCoefficient, confidenceCoefficient, positiveOffset);

        var rows = matrix.GetLength(0);
        var columns = matrix.GetLength(1);
        var minimums = Enumerable.Range(0, rows)
            .Select(i => Enumerable.Range(0, columns).Min(j => matrix[i, j]))
            .ToArray();
        var maximums = Enumerable.Range(0, rows)
            .Select(i => Enumerable.Range(0, columns).Max(j => matrix[i, j]))
            .ToArray();
        var expectations = Enumerable.Range(0, rows)
            .Select(i => Enumerable.Range(0, columns).Sum(j => matrix[i, j] * probabilities[j]))
            .ToArray();

        var hurwicz = Enumerable.Range(0, rows)
            .Select(i => hurwiczCoefficient * minimums[i] + (1 - hurwiczCoefficient) * maximums[i])
            .ToArray();
        var hodgesLehmann = Enumerable.Range(0, rows)
            .Select(i => confidenceCoefficient * expectations[i] + (1 - confidenceCoefficient) * minimums[i])
            .ToArray();
        var germeier = Enumerable.Range(0, rows)
            .Select(i => Enumerable.Range(0, columns).Min(j => matrix[i, j] * probabilities[j]))
            .ToArray();

        var matrixMinimum = matrix.Cast<double>().Min();
        var productShift = matrixMinimum <= 0 ? Math.Abs(matrixMinimum) + positiveOffset : 0;
        var products = Enumerable.Range(0, rows)
            .Select(i => Enumerable.Range(0, columns)
                .Select(j => matrix[i, j] + productShift)
                .Aggregate(1.0, (product, value) => product * value))
            .ToArray();

        return new DerivedDecisionAnalysis(
            CreateMaximumResult("Критерій Гурвіца", hurwicz),
            CreateMaximumResult("Критерій Ходжа-Лемана", hodgesLehmann),
            CreateMaximumResult("Критерій Гермейєра", germeier),
            CreateMaximumResult("Критерій добутків", products),
            minimums,
            maximums,
            expectations,
            productShift);
    }

    public static CriterionResult AnalyzeHurwicz(double[,] matrix, double coefficient)
    {
        ValidateUnitCoefficient(coefficient, nameof(coefficient));
        var rows = matrix.GetLength(0);
        var columns = matrix.GetLength(1);
        var scores = Enumerable.Range(0, rows).Select(i =>
        {
            var values = Enumerable.Range(0, columns).Select(j => matrix[i, j]).ToArray();
            return coefficient * values.Min() + (1 - coefficient) * values.Max();
        }).ToArray();
        return CreateMaximumResult("Критерій Гурвіца", scores);
    }

    public static CriterionResult AnalyzeHodgesLehmann(
        double[,] matrix,
        IReadOnlyList<double> probabilities,
        double confidenceCoefficient)
    {
        ValidateUnitCoefficient(confidenceCoefficient, nameof(confidenceCoefficient));
        if (matrix.GetLength(1) != probabilities.Count)
            throw new ArgumentException("Кількість імовірностей має відповідати кількості станів.");

        var rows = matrix.GetLength(0);
        var columns = matrix.GetLength(1);
        var scores = Enumerable.Range(0, rows).Select(i =>
        {
            var minimum = Enumerable.Range(0, columns).Min(j => matrix[i, j]);
            var expectation = Enumerable.Range(0, columns).Sum(j => matrix[i, j] * probabilities[j]);
            return confidenceCoefficient * expectation + (1 - confidenceCoefficient) * minimum;
        }).ToArray();
        return CreateMaximumResult("Критерій Ходжа-Лемана", scores);
    }

    private static CriterionResult CreateMaximumResult(string name, double[] scores)
    {
        var best = scores.Max();
        var winners = scores.Select((value, index) => (value, index))
            .Where(item => Math.Abs(item.value - best) <= Tolerance)
            .Select(item => item.index + 1)
            .ToArray();
        return new CriterionResult(name, scores, winners);
    }

    private static void Validate(
        double[,] matrix,
        IReadOnlyList<double> probabilities,
        double hurwiczCoefficient,
        double confidenceCoefficient,
        double positiveOffset)
    {
        if (matrix.GetLength(0) == 0 || matrix.GetLength(1) == 0)
            throw new ArgumentException("Матриця не може бути порожньою.", nameof(matrix));
        if (matrix.GetLength(1) != probabilities.Count)
            throw new ArgumentException("Кількість імовірностей має відповідати кількості станів.");
        if (probabilities.Any(p => p < 0) || Math.Abs(probabilities.Sum() - 1) > Tolerance)
            throw new ArgumentException("Імовірності мають бути невід'ємними, а їх сума повинна дорівнювати 1.");
        ValidateUnitCoefficient(hurwiczCoefficient, nameof(hurwiczCoefficient));
        ValidateUnitCoefficient(confidenceCoefficient, nameof(confidenceCoefficient));
        if (positiveOffset <= 0)
            throw new ArgumentOutOfRangeException(nameof(positiveOffset), "Додаткова константа має бути більшою за нуль.");
    }

    private static void ValidateUnitCoefficient(double value, string parameterName)
    {
        if (value is < 0 or > 1)
            throw new ArgumentOutOfRangeException(parameterName, "Коефіцієнт має належати відрізку [0; 1].");
    }
}
