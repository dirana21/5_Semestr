using System.Globalization;
using System.Text;

namespace DecisionTheoryLab1;

public sealed class DecisionAnalyzer
{
    public const int Variant = 12;
    public const int ObjectCount = 15;
    public const int Seed = 12;
    public const double Alpha1 = 0.4;
    public const double Alpha2 = 0.6;
    public const double Alpha3 = 0.1;

    public IReadOnlyList<Alternative> GenerateAlternatives()
    {
        var random = new Random(Seed);
        var result = new List<Alternative>(ObjectCount);
        for (var id = 1; id <= ObjectCount; id++)
        {
            var performance = random.Next(120, 241);
            var cost = random.Next(120, 601);
            var efficiency = Math.Round(1.2 + random.NextDouble() * (120.0 - 1.2), 1);
            result.Add(new Alternative(id, performance, cost, efficiency));
        }
        return result;
    }

    public static bool Dominates(Alternative candidate, Alternative other)
    {
        var noWorse = candidate.Performance >= other.Performance
                      && candidate.Cost <= other.Cost
                      && candidate.Efficiency >= other.Efficiency;
        var strictlyBetter = candidate.Performance > other.Performance
                             || candidate.Cost < other.Cost
                             || candidate.Efficiency > other.Efficiency;
        return noWorse && strictlyBetter;
    }

    public static IReadOnlyList<Alternative> BuildParetoSet(IEnumerable<Alternative> alternatives)
    {
        var list = alternatives.ToList();
        return list.Where(item => !list.Any(candidate =>
                candidate.Id != item.Id && Dominates(candidate, item)))
            .OrderBy(item => item.Id)
            .ToList();
    }

    public static IReadOnlyList<Evaluation> Evaluate(IEnumerable<Alternative> paretoSet)
    {
        var weighted = paretoSet.Select(item => new
        {
            Item = item,
            K1 = item.Performance * Alpha1,
            K2 = item.Cost * Alpha2,
            K3 = item.Efficiency * Alpha3
        }).ToList();

        if (weighted.Count == 0) return [];
        var maxK1 = weighted.Max(x => x.K1);
        var maxK2 = weighted.Max(x => x.K2);
        var maxK3 = weighted.Max(x => x.K3);

        return weighted.Select(x =>
        {
            var n1 = x.K1 / maxK1;
            var n2 = x.K2 / maxK2;
            var n3 = x.K3 / maxK3;
            return new Evaluation(x.Item, x.K1, x.K2, x.K3, n1, n2, n3, n1 - n2 + n3);
        }).OrderByDescending(x => x.Utility).ThenBy(x => x.Alternative.Id).ToList();
    }

    public static void ExportCsv(string path, IEnumerable<Evaluation> evaluations)
    {
        var culture = CultureInfo.InvariantCulture;
        var csv = new StringBuilder("Id;K1;K2;K3;Alpha1K1;Alpha2K2;Alpha3K3;NormK1;NormK2;NormK3;Utility\n");
        foreach (var row in evaluations.OrderBy(x => x.Alternative.Id))
        {
            csv.AppendLine(string.Join(';', row.Alternative.Id,
                row.Alternative.Performance.ToString("0.0", culture),
                row.Alternative.Cost.ToString("0.0", culture),
                row.Alternative.Efficiency.ToString("0.0", culture),
                row.WeightedPerformance.ToString("0.00", culture),
                row.WeightedCost.ToString("0.00", culture),
                row.WeightedEfficiency.ToString("0.00", culture),
                row.NormalizedPerformance.ToString("0.0000", culture),
                row.NormalizedCost.ToString("0.0000", culture),
                row.NormalizedEfficiency.ToString("0.0000", culture),
                row.Utility.ToString("0.0000", culture)));
        }
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, csv.ToString(), new UTF8Encoding(true));
    }
}
