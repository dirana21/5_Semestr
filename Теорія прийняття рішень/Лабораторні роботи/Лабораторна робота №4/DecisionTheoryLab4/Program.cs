using DecisionTheoryLab4;
using System.Globalization;
using System.Text;

Console.OutputEncoding = Encoding.UTF8;
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

Console.WriteLine("ТЕОРІЯ ПРИЙНЯТТЯ РІШЕНЬ — ЛАБОРАТОРНА РОБОТА № 4");
Console.WriteLine("Метод парних порівнянь і метод аналізу ієрархій");
Console.WriteLine("Варіант 12 — вибір району для купівлі квартири\n");
Console.WriteLine("Альтернативи: A1 — Водоканал; A2 — Центр; A3 — Молодіжне.");
Console.WriteLine("Критерії: K1 — вартість; K2 — етажність; K3 — час поїздки до роботи.\n");

PrintAnalysis(Variant12Data.AnalyzeThreePointScale());
PrintAnalysis(Variant12Data.AnalyzeNinePointScale());

static void PrintAnalysis(ScaleAnalysis analysis)
{
    Console.WriteLine($"=== {analysis.ScaleName.ToUpperInvariant()} ===");
    PrintResult(analysis.Criteria, ["K1", "K2", "K3"]);
    for (var index = 0; index < analysis.AlternativesByCriterion.Count; index++)
        PrintResult(analysis.AlternativesByCriterion[index], ["A1", "A2", "A3"]);

    Console.WriteLine("Глобальні пріоритети:");
    for (var index = 0; index < analysis.GlobalPriorities.Count; index++)
        Console.WriteLine($"  A{index + 1} {Variant12Data.Alternatives[index],-10} — {analysis.GlobalPriorities[index]:F6}");
    Console.WriteLine($"Оптимальна альтернатива: A{analysis.BestAlternativeIndex + 1} — {Variant12Data.Alternatives[analysis.BestAlternativeIndex]}\n");
}

static void PrintResult(PairwiseResult result, IReadOnlyList<string> labels)
{
    Console.Write($"{result.Name}: ");
    for (var index = 0; index < result.Priorities.Count; index++)
        Console.Write($"{labels[index]}={result.Priorities[index]:F6} ");
    Console.WriteLine($"| λmax={result.LambdaMax:F6}; ВУ={result.ConsistencyRatio:F6}; узгоджено={(result.IsConsistent ? "так" : "ні")}");
}
