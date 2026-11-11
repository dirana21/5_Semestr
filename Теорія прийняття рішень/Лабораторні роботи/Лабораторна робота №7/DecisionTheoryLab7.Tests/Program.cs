using DecisionTheoryLab7;

var analysis = MatrixGameAnalyzer.Analyze(Variant12Data.Matrix);
var passed = 0;

Check("Початкова матриця має розмір 4 × 4", analysis.OriginalMatrix.GetLength(0) == 4 && analysis.OriginalMatrix.GetLength(1) == 4);
Check("Мінімуми рядків правильні", Same(analysis.OriginalPureAnalysis.RowMinimums, [-5, -3, -3, -5]));
Check("Максимуми стовпців правильні", Same(analysis.OriginalPureAnalysis.ColumnMaximums, [4, 3, 3, 5]));
Check("Нижня ціна дорівнює -3", Close(analysis.OriginalPureAnalysis.LowerValue, -3));
Check("Верхня ціна дорівнює 3", Close(analysis.OriginalPureAnalysis.UpperValue, 3));
Check("Сідлової точки немає", analysis.OriginalPureAnalysis.SaddlePoints.Count == 0);
Check("Стратегію A1 вилучено як доміновану A3", analysis.ReductionSteps.Any(s => s.RemovedStrategy == "A1" && s.DominatingStrategy == "A3"));
Check("Стратегію B1 вилучено як доміновану B2", analysis.ReductionSteps.Any(s => s.RemovedStrategy == "B1" && s.DominatingStrategy == "B2"));
Check("Залишилися рядки A2, A3, A4", analysis.ActiveRows.SequenceEqual([1, 2, 3]));
Check("Залишилися стовпці B2, B3, B4", analysis.ActiveColumns.SequenceEqual([1, 2, 3]));
Check("Скорочена матриця правильна", MatrixSame(analysis.ReducedMatrix, new double[,] { { 3, 0, -3 }, { 0, -3, 4 }, { -5, 3, 5 } }));
Check("Імовірності гравця A правильні", Same(analysis.RowProbabilities, [0, 31.0 / 55, 9.0 / 55, 3.0 / 11]));
Check("Імовірності гравця B правильні", Same(analysis.ColumnProbabilities, [0, 9.0 / 22, 16.0 / 55, 3.0 / 10]));
Check("Сума ймовірностей гравця A дорівнює 1", Close(analysis.RowProbabilities.Sum(), 1));
Check("Сума ймовірностей гравця B дорівнює 1", Close(analysis.ColumnProbabilities.Sum(), 1));
Check("Ціна гри дорівнює 18/55", Close(analysis.GameValue, 18.0 / 55));
Check("Активні стовпці дають значення гри", analysis.ActiveColumns.All(j => Close(analysis.PayoffAgainstColumns[j], analysis.GameValue)));
Check("Вилучений стовпець B1 не кращий для гравця B", analysis.PayoffAgainstColumns[0] >= analysis.GameValue);
Check("Активні рядки дають значення гри", analysis.ActiveRows.All(i => Close(analysis.PayoffForRows[i], analysis.GameValue)));
Check("Вилучений рядок A1 не кращий для гравця A", analysis.PayoffForRows[0] <= analysis.GameValue);

Console.WriteLine($"\nПІДСУМОК: {passed}/20 перевірок виконано успішно.");
Environment.ExitCode = passed == 20 ? 0 : 1;

void Check(string name, bool condition)
{
    Console.WriteLine($"[{(condition ? "PASS" : "FAIL")}] {name}");
    if (condition) passed++;
}

static bool Same(IReadOnlyList<double> actual, IReadOnlyList<double> expected) =>
    actual.Count == expected.Count && actual.Zip(expected).All(pair => Close(pair.First, pair.Second));

static bool MatrixSame(double[,] actual, double[,] expected)
{
    if (actual.GetLength(0) != expected.GetLength(0) || actual.GetLength(1) != expected.GetLength(1)) return false;
    for (var i = 0; i < actual.GetLength(0); i++)
    for (var j = 0; j < actual.GetLength(1); j++)
        if (!Close(actual[i, j], expected[i, j])) return false;
    return true;
}

static bool Close(double left, double right) => Math.Abs(left - right) < 1e-9;
