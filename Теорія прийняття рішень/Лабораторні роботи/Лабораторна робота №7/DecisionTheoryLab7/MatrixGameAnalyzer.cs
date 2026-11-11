namespace DecisionTheoryLab7;

public static class MatrixGameAnalyzer
{
    private const double Tolerance = 1e-9;

    public static MatrixGameAnalysis Analyze(double[,] matrix)
    {
        Validate(matrix);
        var original = (double[,])matrix.Clone();
        var originalPure = AnalyzePureStrategies(original);
        var activeRows = Enumerable.Range(0, matrix.GetLength(0)).ToList();
        var activeColumns = Enumerable.Range(0, matrix.GetLength(1)).ToList();
        var steps = ReduceDominatedStrategies(original, activeRows, activeColumns);
        var reduced = Extract(original, activeRows, activeColumns);
        var reducedPure = AnalyzePureStrategies(reduced);

        if (reducedPure.SaddlePoints.Count > 0)
        {
            var saddle = reducedPure.SaddlePoints[0];
            var rowProbabilities = new double[original.GetLength(0)];
            var columnProbabilities = new double[original.GetLength(1)];
            rowProbabilities[activeRows[saddle.Row]] = 1;
            columnProbabilities[activeColumns[saddle.Column]] = 1;
            var value = reduced[saddle.Row, saddle.Column];
            return CreateResult(original, reduced, activeRows, activeColumns, steps, originalPure,
                reducedPure, rowProbabilities, columnProbabilities, value);
        }

        if (reduced.GetLength(0) != reduced.GetLength(1))
            throw new InvalidOperationException("Після спрощення очікується квадратна матриця для повністю змішаного розв'язку.");

        var (reducedRows, reducedColumns, gameValue) = SolveCompletelyMixedGame(reduced);
        var fullRows = new double[original.GetLength(0)];
        var fullColumns = new double[original.GetLength(1)];
        for (var i = 0; i < activeRows.Count; i++) fullRows[activeRows[i]] = reducedRows[i];
        for (var j = 0; j < activeColumns.Count; j++) fullColumns[activeColumns[j]] = reducedColumns[j];

        return CreateResult(original, reduced, activeRows, activeColumns, steps, originalPure,
            reducedPure, fullRows, fullColumns, gameValue);
    }

    public static PureStrategyAnalysis AnalyzePureStrategies(double[,] matrix)
    {
        Validate(matrix);
        var rows = matrix.GetLength(0);
        var columns = matrix.GetLength(1);
        var rowMinimums = Enumerable.Range(0, rows)
            .Select(i => Enumerable.Range(0, columns).Min(j => matrix[i, j]))
            .ToArray();
        var columnMaximums = Enumerable.Range(0, columns)
            .Select(j => Enumerable.Range(0, rows).Max(i => matrix[i, j]))
            .ToArray();
        var lower = rowMinimums.Max();
        var upper = columnMaximums.Min();
        var saddles = new List<(int Row, int Column)>();

        if (Math.Abs(lower - upper) <= Tolerance)
        {
            for (var i = 0; i < rows; i++)
            for (var j = 0; j < columns; j++)
                if (Math.Abs(matrix[i, j] - lower) <= Tolerance &&
                    Math.Abs(rowMinimums[i] - lower) <= Tolerance &&
                    Math.Abs(columnMaximums[j] - upper) <= Tolerance)
                    saddles.Add((i, j));
        }

        return new PureStrategyAnalysis(rowMinimums, columnMaximums, lower, upper, saddles);
    }

    private static MatrixGameAnalysis CreateResult(
        double[,] original,
        double[,] reduced,
        IReadOnlyList<int> activeRows,
        IReadOnlyList<int> activeColumns,
        IReadOnlyList<DominanceStep> steps,
        PureStrategyAnalysis originalPure,
        PureStrategyAnalysis reducedPure,
        IReadOnlyList<double> rowProbabilities,
        IReadOnlyList<double> columnProbabilities,
        double gameValue)
    {
        var payoffAgainstColumns = Enumerable.Range(0, original.GetLength(1))
            .Select(j => Enumerable.Range(0, original.GetLength(0)).Sum(i => rowProbabilities[i] * original[i, j]))
            .ToArray();
        var payoffForRows = Enumerable.Range(0, original.GetLength(0))
            .Select(i => Enumerable.Range(0, original.GetLength(1)).Sum(j => original[i, j] * columnProbabilities[j]))
            .ToArray();

        return new MatrixGameAnalysis(original, reduced, activeRows.ToArray(), activeColumns.ToArray(),
            steps.ToArray(), originalPure, reducedPure, rowProbabilities.ToArray(), columnProbabilities.ToArray(),
            gameValue, payoffAgainstColumns, payoffForRows);
    }

    private static List<DominanceStep> ReduceDominatedStrategies(
        double[,] matrix,
        List<int> activeRows,
        List<int> activeColumns)
    {
        var steps = new List<DominanceStep>();
        var changed = true;
        while (changed)
        {
            changed = false;
            for (var a = 0; a < activeRows.Count && !changed; a++)
            for (var b = 0; b < activeRows.Count && !changed; b++)
            {
                if (a == b) continue;
                var candidate = activeRows[a];
                var dominator = activeRows[b];
                if (!DominatesRow(matrix, dominator, candidate, activeColumns)) continue;
                steps.Add(new DominanceStep($"A{candidate + 1}", $"A{dominator + 1}",
                    $"Рядок A{dominator + 1} не менший за A{candidate + 1} у кожному активному стовпці."));
                activeRows.RemoveAt(a);
                changed = true;
            }
            if (changed) continue;

            for (var a = 0; a < activeColumns.Count && !changed; a++)
            for (var b = 0; b < activeColumns.Count && !changed; b++)
            {
                if (a == b) continue;
                var candidate = activeColumns[a];
                var dominator = activeColumns[b];
                if (!DominatesColumn(matrix, dominator, candidate, activeRows)) continue;
                steps.Add(new DominanceStep($"B{candidate + 1}", $"B{dominator + 1}",
                    $"Стовпець B{dominator + 1} не більший за B{candidate + 1} у кожному активному рядку."));
                activeColumns.RemoveAt(a);
                changed = true;
            }
        }
        return steps;
    }

    private static bool DominatesRow(double[,] matrix, int dominator, int candidate, IReadOnlyList<int> columns)
    {
        var strictlyBetter = false;
        foreach (var column in columns)
        {
            if (matrix[dominator, column] < matrix[candidate, column] - Tolerance) return false;
            if (matrix[dominator, column] > matrix[candidate, column] + Tolerance) strictlyBetter = true;
        }
        return strictlyBetter;
    }

    private static bool DominatesColumn(double[,] matrix, int dominator, int candidate, IReadOnlyList<int> rows)
    {
        var strictlyBetter = false;
        foreach (var row in rows)
        {
            if (matrix[row, dominator] > matrix[row, candidate] + Tolerance) return false;
            if (matrix[row, dominator] < matrix[row, candidate] - Tolerance) strictlyBetter = true;
        }
        return strictlyBetter;
    }

    private static (double[] Rows, double[] Columns, double Value) SolveCompletelyMixedGame(double[,] matrix)
    {
        var size = matrix.GetLength(0);
        var rowSystem = new double[size + 1, size + 1];
        var rowRight = new double[size + 1];
        for (var equation = 0; equation < size; equation++)
        {
            for (var variable = 0; variable < size; variable++)
                rowSystem[equation, variable] = matrix[variable, equation];
            rowSystem[equation, size] = -1;
        }
        for (var variable = 0; variable < size; variable++) rowSystem[size, variable] = 1;
        rowRight[size] = 1;
        var rowSolution = SolveLinearSystem(rowSystem, rowRight);

        var columnSystem = new double[size + 1, size + 1];
        var columnRight = new double[size + 1];
        for (var equation = 0; equation < size; equation++)
        {
            for (var variable = 0; variable < size; variable++)
                columnSystem[equation, variable] = matrix[equation, variable];
            columnSystem[equation, size] = -1;
        }
        for (var variable = 0; variable < size; variable++) columnSystem[size, variable] = 1;
        columnRight[size] = 1;
        var columnSolution = SolveLinearSystem(columnSystem, columnRight);

        var rows = rowSolution.Take(size).ToArray();
        var columns = columnSolution.Take(size).ToArray();
        if (rows.Any(p => p < -Tolerance) || columns.Any(q => q < -Tolerance))
            throw new InvalidOperationException("Отриманий розв'язок не є повністю змішаним.");
        var value = (rowSolution[size] + columnSolution[size]) / 2;
        return (rows, columns, value);
    }

    private static double[] SolveLinearSystem(double[,] coefficients, double[] right)
    {
        var size = right.Length;
        var augmented = new double[size, size + 1];
        for (var i = 0; i < size; i++)
        {
            for (var j = 0; j < size; j++) augmented[i, j] = coefficients[i, j];
            augmented[i, size] = right[i];
        }

        for (var column = 0; column < size; column++)
        {
            var pivot = Enumerable.Range(column, size - column)
                .MaxBy(row => Math.Abs(augmented[row, column]));
            if (Math.Abs(augmented[pivot, column]) <= Tolerance)
                throw new InvalidOperationException("Система рівнянь має вироджену матрицю.");
            if (pivot != column)
                for (var j = column; j <= size; j++)
                    (augmented[column, j], augmented[pivot, j]) = (augmented[pivot, j], augmented[column, j]);

            var divisor = augmented[column, column];
            for (var j = column; j <= size; j++) augmented[column, j] /= divisor;
            for (var row = 0; row < size; row++)
            {
                if (row == column) continue;
                var factor = augmented[row, column];
                for (var j = column; j <= size; j++) augmented[row, j] -= factor * augmented[column, j];
            }
        }
        return Enumerable.Range(0, size).Select(i => augmented[i, size]).ToArray();
    }

    private static double[,] Extract(double[,] matrix, IReadOnlyList<int> rows, IReadOnlyList<int> columns)
    {
        var result = new double[rows.Count, columns.Count];
        for (var i = 0; i < rows.Count; i++)
        for (var j = 0; j < columns.Count; j++)
            result[i, j] = matrix[rows[i], columns[j]];
        return result;
    }

    private static void Validate(double[,] matrix)
    {
        if (matrix.GetLength(0) == 0 || matrix.GetLength(1) == 0)
            throw new ArgumentException("Платіжна матриця не може бути порожньою.", nameof(matrix));
    }
}
