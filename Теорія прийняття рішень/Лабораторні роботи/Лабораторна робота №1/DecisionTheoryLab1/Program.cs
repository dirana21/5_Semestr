using System.Globalization;
using System.Text;
using DecisionTheoryLab1;

Console.OutputEncoding = Encoding.UTF8;
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

var analyzer = new DecisionAnalyzer();
var alternatives = analyzer.GenerateAlternatives();
var pareto = DecisionAnalyzer.BuildParetoSet(alternatives);
var evaluations = DecisionAnalyzer.Evaluate(pareto);
var best = evaluations.First();

Console.WriteLine("ТЕОРІЯ ПРИЙНЯТТЯ РІШЕНЬ — ЛАБОРАТОРНА РОБОТА № 1");
Console.WriteLine("Варіант 12 | n = 12 | seed = 12 | об'єктів: 15");
Console.WriteLine("Напрямки критеріїв: k1 → max, k2 → min, k3 → max");
Console.WriteLine("Ваги: α1 = 0,4; α2 = 0,6; α3 = 0,1");
Console.WriteLine();
Console.WriteLine("Початкова множина:");
Console.WriteLine(" № |   k1 |   k2 |    k3 | Парето");
Console.WriteLine("---+------+------+-------+-------");
foreach (var item in alternatives)
{
    Console.WriteLine($"{item.Id,2} | {item.Performance,4:0} | {item.Cost,4:0} | {item.Efficiency,5:0.0} | {(pareto.Contains(item) ? "так" : "ні"),6}");
}

Console.WriteLine();
Console.WriteLine($"Множина Парето: {{ {string.Join(", ", pareto.Select(x => x.Id))} }}");
Console.WriteLine();
Console.WriteLine("Нормовані оцінки та функція корисності F = n1 - n2 + n3:");
Console.WriteLine(" № |     n1 |     n2 |     n3 |       F");
Console.WriteLine("---+--------+--------+--------+--------");
foreach (var row in evaluations.OrderBy(x => x.Alternative.Id))
{
    Console.WriteLine($"{row.Alternative.Id,2} | {row.NormalizedPerformance,6:0.0000} | {row.NormalizedCost,6:0.0000} | {row.NormalizedEfficiency,6:0.0000} | {row.Utility,6:0.0000}");
}

Console.WriteLine();
Console.WriteLine($"Оптимальне рішення: об'єкт № {best.Alternative.Id}, Fmax = {best.Utility:0.0000}");
var outputPath = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "results", "pareto-results.csv"));
DecisionAnalyzer.ExportCsv(outputPath, evaluations);
Console.WriteLine($"Результати збережено: {outputPath}");
