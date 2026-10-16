using System.Globalization;
using System.Text;
using DecisionTheoryLab2;

Console.OutputEncoding = Encoding.UTF8;
CultureInfo.CurrentCulture = CultureInfo.GetCultureInfo("uk-UA");

var data = Lab2Analyzer.GetVariant12Data();
var result = Lab2Analyzer.Analyze(data);

Console.WriteLine("ТЕОРІЯ ПРИЙНЯТТЯ РІШЕНЬ — ЛАБОРАТОРНА РОБОТА № 2");
Console.WriteLine("Варіант 12 | 4 об'єкти | 3 експерти");
Console.WriteLine();
Console.WriteLine("Первинні оцінки:");
Console.WriteLine(" № | Бали експертів | Ранги експертів");
Console.WriteLine("---+----------------+----------------");
foreach (var item in data)
{
    Console.WriteLine($"{item.ObjectId,2} | {string.Join("; ", item.Scores.Select(x => x.ToString("0.#"))),-14} | {string.Join("; ", item.Ranks.Select(x => x.ToString("0.#")))}");
}

Console.WriteLine();
Console.WriteLine("Середні та медіанні рангові оцінки:");
Console.WriteLine(" № | Σr   | середнє | медіана | Rсер | Rмед");
Console.WriteLine("---+------+---------+---------+------+-----");
foreach (var row in result.Objects)
{
    Console.WriteLine($"{row.ObjectId,2} | {row.RankSum,4:0.0} | {row.AverageRank,7:0.0000} | {row.MedianRank,7:0.0000} | {row.FinalAverageRank,4:0.#} | {row.FinalMedianRank,4:0.#}");
}

Console.WriteLine();
Console.WriteLine("Коефіцієнти вагомості:");
Console.WriteLine(" № | за балами | за рангами");
Console.WriteLine("---+-----------+-----------");
foreach (var row in result.Objects)
{
    Console.WriteLine($"{row.ObjectId,2} | {row.ScoreWeight,9:0.000000} | {row.RankWeight,9:0.000000}");
}

Console.WriteLine();
Console.WriteLine($"S = {result.SquaredDeviationSum:0.0000}");
Console.WriteLine($"W = {result.Concordance:0.0000}");
Console.WriteLine(result.IsConcordant
    ? "Висновок: W ≥ 0,5 — думки експертів узгоджені, дані придатні до використання."
    : "Висновок: W < 0,5 — узгодженість недостатня.");
Console.WriteLine("Підсумковий порядок за середніми та медіанами: 4 → 3 → 2 → 1.");

var outputPath = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "results", "lab2-results.csv"));
Lab2Analyzer.ExportCsv(outputPath, result);
