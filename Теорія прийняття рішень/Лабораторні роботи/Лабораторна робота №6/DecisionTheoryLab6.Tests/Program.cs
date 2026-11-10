using DecisionTheoryLab6;

var matrix = Variant12Data.Matrix;
var probabilities = Variant12Data.Probabilities;
var analysis = DerivedDecisionAnalyzer.Analyze(
    matrix,
    probabilities,
    Variant12Data.HurwiczCoefficient,
    Variant12Data.ConfidenceCoefficient,
    Variant12Data.PositiveOffset);
var passed = 0;

Check("Матриця має розмір 8 × 8", matrix.GetLength(0) == 8 && matrix.GetLength(1) == 8);
Check("Сума імовірностей дорівнює 1", Close(probabilities.Sum(), 1));
Check("Мінімуми рядків правильні", Same(analysis.RowMinimums, [-0.77, -0.93, -0.93, -0.64, -0.96, -0.75, -0.94, -0.95]));
Check("Максимуми рядків правильні", Same(analysis.RowMaximums, [-0.02, -0.01, -0.03, -0.01, -0.15, -0.03, -0.06, -0.01]));
Check("Математичні сподівання правильні", Same(analysis.Expectations, [-0.4888, -0.4165, -0.3860, -0.3603, -0.4090, -0.4775, -0.5640, -0.5520]));
Check("Оцінки Гурвіца правильні", Same(analysis.Hurwicz.Scores, [-0.2450, -0.2860, -0.3000, -0.1990, -0.3930, -0.2460, -0.3240, -0.2920]));
Check("Критерій Гурвіца обирає E4", analysis.Hurwicz.OptimalAlternatives.SequenceEqual([4]));
Check("Оцінки Ходжа-Лемана правильні", Same(analysis.HodgesLehmann.Scores, [-0.6294, -0.67325, -0.6580, -0.50015, -0.6845, -0.61375, -0.7520, -0.7510]));
Check("Критерій Ходжа-Лемана обирає E4", analysis.HodgesLehmann.OptimalAlternatives.SequenceEqual([4]));
Check("Оцінки Гермейєра правильні", Same(analysis.Germeier.Scores, [-0.210, -0.150, -0.093, -0.078, -0.096, -0.225, -0.276, -0.225]));
Check("Критерій Гермейєра обирає E4", analysis.Germeier.OptimalAlternatives.SequenceEqual([4]));
Check("Зсув для добутків дорівнює 1,46", Close(analysis.ProductShift, 1.46));
Check("Оцінки добутків правильні", Same(analysis.Product.Scores, [0.9060112512, 1.1457676000, 0.6167438842, 1.5206882372, 0.6057909403, 1.1138470407, 0.5495085542, 0.4177026165], 1e-8));
Check("Критерій добутків обирає E4", analysis.Product.OptimalAlternatives.SequenceEqual([4]));
Check("При C=0 оптимальні E2, E4 та E8", DerivedDecisionAnalyzer.AnalyzeHurwicz(matrix, 0).OptimalAlternatives.SequenceEqual([2, 4, 8]));
Check("При C>0 оптимальною є E4", Enumerable.Range(1, 100).All(i => DerivedDecisionAnalyzer.AnalyzeHurwicz(matrix, i / 100.0).OptimalAlternatives.SequenceEqual([4])));
Check("Для всіх v оптимальною є E4", Enumerable.Range(0, 101).All(i => DerivedDecisionAnalyzer.AnalyzeHodgesLehmann(matrix, probabilities, i / 100.0).OptimalAlternatives.SequenceEqual([4])));
Check("Усі критерії за заданими параметрами обирають E4", new[] { analysis.Hurwicz, analysis.HodgesLehmann, analysis.Germeier, analysis.Product }.All(result => result.OptimalAlternatives.SequenceEqual([4])));

Console.WriteLine($"\nПІДСУМОК: {passed}/18 перевірок виконано успішно.");
Environment.ExitCode = passed == 18 ? 0 : 1;

void Check(string name, bool condition)
{
    Console.WriteLine($"[{(condition ? "PASS" : "FAIL")}] {name}");
    if (condition) passed++;
}

static bool Same(IReadOnlyList<double> actual, IReadOnlyList<double> expected, double tolerance = 1e-9) =>
    actual.Count == expected.Count && actual.Zip(expected).All(pair => Close(pair.First, pair.Second, tolerance));

static bool Close(double left, double right, double tolerance = 1e-9) => Math.Abs(left - right) < tolerance;
