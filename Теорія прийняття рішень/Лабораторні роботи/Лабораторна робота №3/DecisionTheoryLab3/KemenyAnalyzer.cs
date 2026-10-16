namespace DecisionTheoryLab3;

public static class KemenyAnalyzer
{
    public static KemenyAnalysis Analyze(IReadOnlyList<ExpertRelation> relations)
    {
        if (relations.Count == 0)
            throw new ArgumentException("Потрібна хоча б одна експертна матриця.", nameof(relations));

        foreach (var relation in relations)
            ValidateBinaryRelation(relation.Matrix);

        var distances = new int[relations.Count, relations.Count];
        for (var i = 0; i < relations.Count; i++)
        for (var j = i + 1; j < relations.Count; j++)
        {
            var distance = KemenyDistance(relations[i].Matrix, relations[j].Matrix);
            distances[i, j] = distance;
            distances[j, i] = distance;
        }

        var candidates = new List<CandidateResult>();
        for (var candidate = 0; candidate < relations.Count; candidate++)
        {
            var total = 0;
            var squared = 0;
            for (var expert = 0; expert < relations.Count; expert++)
            {
                var distance = distances[expert, candidate];
                total += distance;
                squared += distance * distance;
            }

            candidates.Add(new CandidateResult(
                relations[candidate].ExpertNumber,
                total,
                squared));
        }

        var minimumTotal = candidates.Min(candidate => candidate.TotalDistance);
        var minimumSquared = candidates.Min(candidate => candidate.TotalSquaredDistance);
        var medianExperts = candidates
            .Where(candidate => candidate.TotalDistance == minimumTotal)
            .Select(candidate => candidate.ExpertNumber)
            .ToArray();
        var meanExperts = candidates
            .Where(candidate => candidate.TotalSquaredDistance == minimumSquared)
            .Select(candidate => candidate.ExpertNumber)
            .ToArray();
        var consensus = CloneMatrix(relations.First(
            relation => relation.ExpertNumber == medianExperts[0]).Matrix);

        return new KemenyAnalysis(
            distances,
            candidates,
            medianExperts,
            meanExperts,
            consensus);
    }

    public static int KemenyDistance(int[,] left, int[,] right)
    {
        EnsureSameDimensions(left, right);
        var distance = 0;
        for (var row = 0; row < left.GetLength(0); row++)
        for (var column = 0; column < left.GetLength(1); column++)
            distance += Math.Abs(left[row, column] - right[row, column]);
        return distance;
    }

    public static void ValidateBinaryRelation(int[,] matrix)
    {
        if (matrix.GetLength(0) != matrix.GetLength(1))
            throw new ArgumentException("Матриця бінарного відношення має бути квадратною.");

        var size = matrix.GetLength(0);
        for (var row = 0; row < size; row++)
        for (var column = 0; column < size; column++)
        {
            if (matrix[row, column] is not (0 or 1))
                throw new ArgumentException("Матриця має містити лише 0 та 1.");
            if (row == column && matrix[row, column] != 0)
                throw new ArgumentException("На головній діагоналі мають бути нулі.");
            if (row != column && matrix[row, column] + matrix[column, row] != 1)
                throw new ArgumentException("Для кожної пари альтернатив має виконуватися взаємна доповнюваність.");
        }
    }

    private static void EnsureSameDimensions(int[,] left, int[,] right)
    {
        if (left.GetLength(0) != right.GetLength(0) ||
            left.GetLength(1) != right.GetLength(1))
            throw new ArgumentException("Матриці повинні мати однаковий розмір.");
    }

    private static int[,] CloneMatrix(int[,] source) => (int[,])source.Clone();
}
