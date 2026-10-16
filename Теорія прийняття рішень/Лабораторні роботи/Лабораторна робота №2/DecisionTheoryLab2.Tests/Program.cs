using System.Text;
using DecisionTheoryLab2;

Console.OutputEncoding = Encoding.UTF8;
var failures = new List<string>();
void Check(string name, bool condition)
{
    Console.WriteLine($"[{(condition ? "PASS" : "FAIL")}] {name}");
    if (!condition) failures.Add(name);
}

var data = Lab2Analyzer.GetVariant12Data();
var result = Lab2Analyzer.Analyze(data);
var byId = result.Objects.ToDictionary(x => x.ObjectId);
const double tolerance = 1e-6;

Console.WriteLine("АВТОМАТИЧНА ПЕРЕВІРКА ЛАБОРАТОРНОЇ РОБОТИ № 2");
Console.WriteLine();
Check("Завантажено 4 об'єкти та 3 експертні оцінки", data.Count == 4 && data.All(x => x.Scores.Count == 3 && x.Ranks.Count == 3));
Check("Сума балів дорівнює 37", Math.Abs(result.Objects.Sum(x => x.ScoreSum) - 37) < tolerance);
Check("Сума ваг за балами дорівнює 1", Math.Abs(result.Objects.Sum(x => x.ScoreWeight) - 1) < tolerance);
Check("Суми рангів експертів дорівнюють 10", Enumerable.Range(0, 3).All(j => Math.Abs(data.Sum(x => x.Ranks[j]) - 10) < tolerance));
Check("Середні ранги обчислено правильно", Math.Abs(byId[1].AverageRank - 11.5 / 3) < tolerance && Math.Abs(byId[4].AverageRank - 4.0 / 3) < tolerance);
Check("Медіани рангів дорівнюють 4, 3, 2, 1", byId[1].MedianRank == 4 && byId[2].MedianRank == 3 && byId[3].MedianRank == 2 && byId[4].MedianRank == 1);
Check("Обидва способи дають порядок 4 → 3 → 2 → 1", result.Objects.OrderBy(x => x.FinalAverageRank).Select(x => x.ObjectId).SequenceEqual([4, 3, 2, 1]) && result.Objects.OrderBy(x => x.FinalMedianRank).Select(x => x.ObjectId).SequenceEqual([4, 3, 2, 1]));
Check("Сума ваг за рангами дорівнює 1", Math.Abs(result.Objects.Sum(x => x.RankWeight) - 1) < tolerance);
Check("Сума відхилень дорівнює 0", Math.Abs(result.Objects.Sum(x => x.Deviation)) < tolerance);
Check("Сума квадратів відхилень S = 31,5", Math.Abs(result.SquaredDeviationSum - 31.5) < tolerance);
Check("Коефіцієнт конкордації W = 0,7", Math.Abs(result.Concordance - 0.7) < tolerance);
Check("Узгодженість експертів достатня", result.IsConcordant);

Console.WriteLine();
Console.WriteLine(failures.Count == 0
    ? "ПІДСУМОК: 12/12 перевірок виконано успішно."
    : $"ПІДСУМОК: помилок — {failures.Count}.");
return failures.Count == 0 ? 0 : 1;
