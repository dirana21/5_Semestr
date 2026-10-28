using System.Globalization;
using DecisionTheoryLab5;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");
var matrix = Variant12Data.Matrix;
var probabilities = Variant12Data.Probabilities;
var analysis = ClassicalDecisionAnalyzer.Analyze(matrix, probabilities);
var section = args.SkipWhile(arg => arg != "--section").Skip(1).FirstOrDefault() ?? "all";

Console.WriteLine("ТЕОРІЯ ПРИЙНЯТТЯ РІШЕНЬ — ЛАБОРАТОРНА РОБОТА № 5");
Console.WriteLine("Класичні критерії прийняття рішень. Варіант 12.");

if (section is "input" or "all")
{
    Console.WriteLine("\nМатриця рішень (8 альтернатив × 8 станів):");
    Console.WriteLine("       F1      F2      F3      F4      F5      F6      F7      F8");
    for (var i = 0; i < matrix.GetLength(0); i++)
    {
        Console.Write($"E{i + 1} ");
        for (var j = 0; j < matrix.GetLength(1); j++) Console.Write($"{matrix[i, j],8:0.000}");
        Console.WriteLine();
    }
    Console.WriteLine("\nІмовірності: " + string.Join("; ", probabilities.Select((p, i) => $"p{i + 1}={p:0.0}")));
    PrintResult(analysis.Minimax);
}

if (section is "criteria" or "all")
{
    Console.WriteLine();
    PrintResult(analysis.BayesLaplace);
    PrintResult(analysis.Savage);
    Console.WriteLine("\nУсі три критерії рекомендують альтернативу E4.");
}

static void PrintResult(CriterionResult result)
{
    Console.WriteLine($"\n{result.Name}:");
    Console.WriteLine(string.Join("  ", result.Scores.Select((score, i) => $"E{i + 1}={score:0.0000}")));
    Console.WriteLine("Оптимальна альтернатива: " + string.Join(", ", result.OptimalAlternatives.Select(i => $"E{i}")));
}
