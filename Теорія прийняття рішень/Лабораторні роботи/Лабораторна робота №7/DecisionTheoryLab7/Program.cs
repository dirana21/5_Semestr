using System.Globalization;
using DecisionTheoryLab7;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");
var analysis = MatrixGameAnalyzer.Analyze(Variant12Data.Matrix);
var section = args.SkipWhile(arg => arg != "--section").Skip(1).FirstOrDefault() ?? "all";

Console.WriteLine("ТЕОРІЯ ПРИЙНЯТТЯ РІШЕНЬ — ЛАБОРАТОРНА РОБОТА № 7");
Console.WriteLine("Матрична гра з нульовою сумою. Варіант 12.");

if (section is "input" or "all")
{
    Console.WriteLine("\nПочаткова платіжна матриця:");
    PrintMatrix(analysis.OriginalMatrix, [1, 2, 3, 4], [1, 2, 3, 4]);
    Console.WriteLine("\nМінімуми рядків: " + FormatVector(analysis.OriginalPureAnalysis.RowMinimums, "A"));
    Console.WriteLine("Максимуми стовпців: " + FormatVector(analysis.OriginalPureAnalysis.ColumnMaximums, "B"));
    Console.WriteLine($"Нижня ціна α = {analysis.OriginalPureAnalysis.LowerValue:0.###}");
    Console.WriteLine($"Верхня ціна β = {analysis.OriginalPureAnalysis.UpperValue:0.###}");
    Console.WriteLine("Оскільки α ≠ β, сідлової точки немає.");
}

if (section is "reduction" or "all")
{
    Console.WriteLine("\nСПРОЩЕННЯ МАТРИЦІ");
    foreach (var step in analysis.ReductionSteps)
        Console.WriteLine($"{step.RemovedStrategy} вилучено: домінує {step.DominatingStrategy}.");
    Console.WriteLine("\nСкорочена матриця:");
    PrintMatrix(analysis.ReducedMatrix,
        analysis.ActiveRows.Select(i => i + 1).ToArray(),
        analysis.ActiveColumns.Select(i => i + 1).ToArray());
}

if (section is "solution" or "all")
{
    Console.WriteLine("\nОПТИМАЛЬНІ ЗМІШАНІ СТРАТЕГІЇ");
    Console.WriteLine("Гравець A: " + FormatProbabilities(analysis.RowProbabilities, "A"));
    Console.WriteLine("Гравець B: " + FormatProbabilities(analysis.ColumnProbabilities, "B"));
    Console.WriteLine($"Ціна гри: v = 18/55 = {analysis.GameValue:0.000000}");
    Console.WriteLine("\nПеревірка pᵀA за стовпцями: " + FormatVector(analysis.PayoffAgainstColumns, "B", 6));
    Console.WriteLine("Перевірка Aq за рядками: " + FormatVector(analysis.PayoffForRows, "A", 6));
    Console.WriteLine("Активні стратегії дають однакове очікуване значення v.");
}

static void PrintMatrix(double[,] matrix, IReadOnlyList<int> rowNames, IReadOnlyList<int> columnNames)
{
    Console.Write("      ");
    foreach (var column in columnNames) Console.Write($"{($"B{column}"),8}");
    Console.WriteLine();
    for (var i = 0; i < matrix.GetLength(0); i++)
    {
        Console.Write($"A{rowNames[i]} ");
        for (var j = 0; j < matrix.GetLength(1); j++) Console.Write($"{matrix[i, j],8:0.###}");
        Console.WriteLine();
    }
}

static string FormatVector(IReadOnlyList<double> values, string prefix, int digits = 3) =>
    string.Join("; ", values.Select((value, i) => $"{prefix}{i + 1}={value.ToString($"0.{new string('#', digits)}")}"));

static string FormatProbabilities(IReadOnlyList<double> values, string prefix) =>
    string.Join("; ", values.Select((value, i) => $"{prefix}{i + 1}={AsFraction(value)} ({value:0.000000})"));

static string AsFraction(double value)
{
    for (var denominator = 1; denominator <= 220; denominator++)
    {
        var numerator = (int)Math.Round(value * denominator);
        if (Math.Abs(value - (double)numerator / denominator) < 1e-8)
            return denominator == 1 ? numerator.ToString() : $"{numerator}/{denominator}";
    }
    return value.ToString("0.######");
}
