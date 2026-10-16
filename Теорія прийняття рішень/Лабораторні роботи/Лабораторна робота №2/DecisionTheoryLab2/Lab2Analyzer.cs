using System.Globalization;
using System.Text;

namespace DecisionTheoryLab2;

public static class Lab2Analyzer
{
    public const int Variant = 12;

    public static IReadOnlyList<ExpertEvaluation> GetVariant12Data() =>
    [
        new(1, [1, 1, 1], [3.5, 4, 4]),
        new(2, [3, 4, 3], [3.5, 3, 2]),
        new(3, [5, 5, 4], [1, 2, 3]),
        new(4, [4, 3, 3], [2, 1, 1])
    ];

    public static AnalysisResult Analyze(IReadOnlyList<ExpertEvaluation> data)
    {
        if (data.Count == 0) throw new ArgumentException("Потрібна хоча б одна оцінювана альтернатива.", nameof(data));
        var expertCount = data[0].Scores.Count;
        if (expertCount == 0 || data.Any(x => x.Scores.Count != expertCount || x.Ranks.Count != expertCount))
            throw new ArgumentException("Усі об'єкти повинні мати однакову ненульову кількість оцінок експертів.", nameof(data));

        var scoreSums = data.ToDictionary(x => x.ObjectId, x => x.Scores.Sum());
        var totalScore = scoreSums.Values.Sum();
        var rankSums = data.ToDictionary(x => x.ObjectId, x => x.Ranks.Sum());
        var averages = data.ToDictionary(x => x.ObjectId, x => x.Ranks.Average());
        var medians = data.ToDictionary(x => x.ObjectId, x => Median(x.Ranks));
        var finalAverageRanks = RankAscending(averages);
        var finalMedianRanks = RankAscending(medians);

        var objectCount = data.Count;
        var meanRankSum = rankSums.Values.Average();
        var rankWeightDenominator = 0.5 * expertCount * objectCount * (objectCount - 1);

        var objects = data.Select(x =>
        {
            var deviation = rankSums[x.ObjectId] - meanRankSum;
            return new ObjectResult(
                x.ObjectId,
                scoreSums[x.ObjectId],
                scoreSums[x.ObjectId] / totalScore,
                rankSums[x.ObjectId],
                averages[x.ObjectId],
                medians[x.ObjectId],
                finalAverageRanks[x.ObjectId],
                finalMedianRanks[x.ObjectId],
                (expertCount * objectCount - rankSums[x.ObjectId]) / rankWeightDenominator,
                deviation,
                deviation * deviation);
        }).OrderBy(x => x.ObjectId).ToList();

        var squaredDeviationSum = objects.Sum(x => x.SquaredDeviation);
        var concordance = 12 * squaredDeviationSum /
                          (expertCount * expertCount * (Math.Pow(objectCount, 3) - objectCount));

        return new AnalysisResult(objects, meanRankSum, squaredDeviationSum, concordance, concordance >= 0.5);
    }

    public static double Median(IEnumerable<double> values)
    {
        var ordered = values.OrderBy(x => x).ToArray();
        if (ordered.Length == 0) throw new ArgumentException("Медіану порожньої множини не визначено.", nameof(values));
        var middle = ordered.Length / 2;
        return ordered.Length % 2 == 1
            ? ordered[middle]
            : (ordered[middle - 1] + ordered[middle]) / 2;
    }

    private static Dictionary<int, double> RankAscending(IReadOnlyDictionary<int, double> values)
    {
        var ordered = values.OrderBy(x => x.Value).ThenBy(x => x.Key).ToList();
        var result = new Dictionary<int, double>();
        var index = 0;
        while (index < ordered.Count)
        {
            var end = index + 1;
            while (end < ordered.Count && Math.Abs(ordered[end].Value - ordered[index].Value) < 1e-10) end++;
            var averagePosition = ((index + 1) + end) / 2.0;
            for (var i = index; i < end; i++) result[ordered[i].Key] = averagePosition;
            index = end;
        }
        return result;
    }

    public static void ExportCsv(string path, AnalysisResult result)
    {
        var culture = CultureInfo.InvariantCulture;
        var csv = new StringBuilder("Object;ScoreSum;ScoreWeight;RankSum;AverageRank;MedianRank;FinalAverageRank;FinalMedianRank;RankWeight;Deviation;SquaredDeviation\n");
        foreach (var row in result.Objects)
        {
            csv.AppendLine(string.Join(';',
                row.ObjectId,
                row.ScoreSum.ToString("0.####", culture),
                row.ScoreWeight.ToString("0.######", culture),
                row.RankSum.ToString("0.####", culture),
                row.AverageRank.ToString("0.######", culture),
                row.MedianRank.ToString("0.######", culture),
                row.FinalAverageRank.ToString("0.####", culture),
                row.FinalMedianRank.ToString("0.####", culture),
                row.RankWeight.ToString("0.######", culture),
                row.Deviation.ToString("0.####", culture),
                row.SquaredDeviation.ToString("0.####", culture)));
        }
        csv.AppendLine($"Concordance;{result.Concordance.ToString("0.######", culture)}");
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        File.WriteAllText(path, csv.ToString(), new UTF8Encoding(true));
    }
}
