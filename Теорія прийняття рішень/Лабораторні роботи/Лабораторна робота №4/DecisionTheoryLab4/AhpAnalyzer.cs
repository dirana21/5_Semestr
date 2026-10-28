namespace DecisionTheoryLab4;

public static class AhpAnalyzer
{
    private static readonly IReadOnlyDictionary<int, double> RandomIndex =
        new Dictionary<int, double>
        {
            [1] = 0,
            [2] = 0,
            [3] = 0.58,
            [4] = 0.90,
            [5] = 1.12,
            [6] = 1.24,
            [7] = 1.32,
            [8] = 1.41,
            [9] = 1.45,
            [10] = 1.49
        };

    public static PairwiseResult Analyze(string name, double[,] matrix)
    {
        Validate(matrix);
        var size = matrix.GetLength(0);
        var geometricMeans = new double[size];
        for (var row = 0; row < size; row++)
        {
            var product = 1.0;
            for (var column = 0; column < size; column++)
                product *= matrix[row, column];
            geometricMeans[row] = Math.Pow(product, 1.0 / size);
        }

        var total = geometricMeans.Sum();
        var priorities = geometricMeans.Select(value => value / total).ToArray();
        var columnSums = new double[size];
        for (var column = 0; column < size; column++)
        for (var row = 0; row < size; row++)
            columnSums[column] += matrix[row, column];

        var lambdaMax = priorities.Select((priority, index) => priority * columnSums[index]).Sum();
        var consistencyIndex = size <= 2 ? 0 : (lambdaMax - size) / (size - 1);
        var randomIndex = RandomIndex.TryGetValue(size, out var value) ? value : throw new ArgumentException("Немає випадкового індексу для цього розміру матриці.");
        var consistencyRatio = randomIndex == 0 ? 0 : consistencyIndex / randomIndex;

        return new PairwiseResult(name, priorities, lambdaMax, consistencyIndex, consistencyRatio);
    }

    public static IReadOnlyList<double> Aggregate(
        IReadOnlyList<double> criteriaPriorities,
        IReadOnlyList<PairwiseResult> alternativesByCriterion)
    {
        if (criteriaPriorities.Count != alternativesByCriterion.Count)
            throw new ArgumentException("Кількість ваг критеріїв не відповідає кількості локальних векторів.");

        var alternativeCount = alternativesByCriterion[0].Priorities.Count;
        var global = new double[alternativeCount];
        for (var alternative = 0; alternative < alternativeCount; alternative++)
        for (var criterion = 0; criterion < criteriaPriorities.Count; criterion++)
            global[alternative] += criteriaPriorities[criterion] * alternativesByCriterion[criterion].Priorities[alternative];
        return global;
    }

    public static void Validate(double[,] matrix)
    {
        if (matrix.GetLength(0) != matrix.GetLength(1))
            throw new ArgumentException("Матриця парних порівнянь має бути квадратною.");

        var size = matrix.GetLength(0);
        for (var row = 0; row < size; row++)
        for (var column = 0; column < size; column++)
        {
            if (matrix[row, column] <= 0)
                throw new ArgumentException("Усі елементи матриці мають бути додатними.");
            if (row == column && Math.Abs(matrix[row, column] - 1) > 1e-9)
                throw new ArgumentException("На головній діагоналі мають бути одиниці.");
            if (Math.Abs(matrix[row, column] * matrix[column, row] - 1) > 1e-9)
                throw new ArgumentException("Матриця має бути обернено симетричною.");
        }
    }
}
