using DecisionTheoryLab5;

var matrix = Variant12Data.Matrix;
var probabilities = Variant12Data.Probabilities;
var analysis = ClassicalDecisionAnalyzer.Analyze(matrix, probabilities);
var passed = 0;

Check("Матриця має розмір 8 × 8", matrix.GetLength(0) == 8 && matrix.GetLength(1) == 8);
Check("Задано вісім імовірностей", probabilities.Length == 8);
Check("Сума імовірностей дорівнює 1", Close(probabilities.Sum(), 1));
Check("Мінімуми рядків обчислено правильно", Same(analysis.Minimax.Scores, [-0.77, -0.93, -0.93, -0.64, -0.96, -0.75, -0.94, -0.95]));
Check("За мінімаксним критерієм обрано E4", analysis.Minimax.OptimalAlternatives.SequenceEqual([4]));
Check("Мінімаксне значення дорівнює -0,64", Close(analysis.Minimax.Scores[3], -0.64));
Check("Математичні сподівання обчислено правильно", Same(analysis.BayesLaplace.Scores, [-0.4888, -0.4165, -0.3860, -0.3603, -0.4090, -0.4775, -0.5640, -0.5520]));
Check("За критерієм Байєса-Лапласа обрано E4", analysis.BayesLaplace.OptimalAlternatives.SequenceEqual([4]));
Check("Найкраще сподівання дорівнює -0,3603", Close(analysis.BayesLaplace.Scores[3], -0.3603));
Check("Максимуми стовпців обчислено правильно", Same(analysis.ColumnMaxima, [-0.03, -0.01, -0.06, -0.01, -0.01, -0.06, -0.02, -0.01]));
Check("Матриця ризиків має розмір 8 × 8", analysis.RegretMatrix.GetLength(0) == 8 && analysis.RegretMatrix.GetLength(1) == 8);
Check("Контрольний елемент матриці ризиків правильний", Close(analysis.RegretMatrix[3, 6], 0.62));
Check("Максимальні ризики обчислено правильно", Same(analysis.Savage.Scores, [0.76, 0.87, 0.87, 0.62, 0.95, 0.72, 0.92, 0.94]));
Check("За критерієм Севіджа обрано E4", analysis.Savage.OptimalAlternatives.SequenceEqual([4]));
Check("Усі критерії дали однакове рішення", new[] { analysis.Minimax, analysis.BayesLaplace, analysis.Savage }.All(r => r.OptimalAlternatives.SequenceEqual([4])));

Console.WriteLine($"\nПІДСУМОК: {passed}/15 перевірок виконано успішно.");
Environment.ExitCode = passed == 15 ? 0 : 1;

void Check(string name, bool condition)
{
    Console.WriteLine($"[{(condition ? "PASS" : "FAIL")}] {name}");
    if (condition) passed++;
}

static bool Same(IReadOnlyList<double> actual, IReadOnlyList<double> expected) =>
    actual.Count == expected.Count && actual.Zip(expected).All(pair => Close(pair.First, pair.Second));

static bool Close(double left, double right) => Math.Abs(left - right) < 1e-9;
