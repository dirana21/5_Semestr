using System.Globalization;
using DecisionTheoryLab6;

CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

var matrix = Variant12Data.Matrix;
var probabilities = Variant12Data.Probabilities;
var analysis = DerivedDecisionAnalyzer.Analyze(
    matrix,
    probabilities,
    Variant12Data.HurwiczCoefficient,
    Variant12Data.ConfidenceCoefficient,
    Variant12Data.PositiveOffset);
var section = args.SkipWhile(arg => arg != "--section").Skip(1).FirstOrDefault() ?? "all";

Console.WriteLine("ТЕОРІЯ ПРИЙНЯТТЯ РІШЕНЬ — ЛАБОРАТОРНА РОБОТА № 6");
Console.WriteLine("Похідні критерії прийняття рішень. Варіант 12.");
Console.WriteLine("Параметри: C=0,3; v=0,5; εдоп=0,5.");

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
    PrintResult(analysis.Hurwicz);
    PrintResult(analysis.HodgesLehmann);
}

if (section is "criteria" or "all")
{
    Console.WriteLine($"\nЗсув для критерію добутків: a = |−0,96| + 0,5 = {analysis.ProductShift:0.00}");
    PrintResult(analysis.Germeier);
    PrintResult(analysis.Product);
    Console.WriteLine("\nУсі чотири критерії рекомендують альтернативу E4.");
}

if (section is "sensitivity" or "all")
{
    Console.WriteLine("\nАНАЛІЗ ПОВОРОТНИХ ЗНАЧЕНЬ");
    Console.WriteLine("Гурвіц: при C=0 оптимальні E2, E4 та E8; для будь-якого C>0 оптимальна E4.");
    Console.WriteLine("Ходж-Леман: на всьому відрізку 0≤v≤1 оптимальною залишається E4.");
}

static void PrintResult(CriterionResult result)
{
    Console.WriteLine($"\n{result.Name}:");
    Console.WriteLine(string.Join("  ", result.Scores.Select((score, i) => $"E{i + 1}={score:0.000000}")));
    Console.WriteLine("Оптимальна альтернатива: " + string.Join(", ", result.OptimalAlternatives.Select(i => $"E{i}")));
}
