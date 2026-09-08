using System.Text;
using DecisionTheoryLab1;

Console.OutputEncoding = Encoding.UTF8;
var failures = new List<string>();
void Check(string name, bool condition)
{
    Console.WriteLine($"[{(condition ? "PASS" : "FAIL")}] {name}");
    if (!condition) failures.Add(name);
}

var analyzer = new DecisionAnalyzer();
var generated = analyzer.GenerateAlternatives();
var generatedAgain = analyzer.GenerateAlternatives();
var pareto = DecisionAnalyzer.BuildParetoSet(generated);
var evaluations = DecisionAnalyzer.Evaluate(pareto);

Console.WriteLine("АВТОМАТИЧНА ПЕРЕВІРКА ЛАБОРАТОРНОЇ РОБОТИ № 1");
Console.WriteLine();
Check("Створено рівно 15 об'єктів", generated.Count == 15);
Check("Генерація відтворювана для seed = 12", generated.SequenceEqual(generatedAgain));
Check("Усі k1 належать [120; 240]", generated.All(x => x.Performance is >= 120 and <= 240));
Check("Усі k2 належать [120; 600]", generated.All(x => x.Cost is >= 120 and <= 600));
Check("Усі k3 належать [1,2; 120]", generated.All(x => x.Efficiency is >= 1.2 and <= 120));
Check("У множині Парето немає домінованих об'єктів", pareto.All(item =>
    !generated.Any(candidate => candidate.Id != item.Id && DecisionAnalyzer.Dominates(candidate, item))));
Check("Кожен вилучений об'єкт домінується хоча б одним іншим", generated.Except(pareto).All(item =>
    generated.Any(candidate => candidate.Id != item.Id && DecisionAnalyzer.Dominates(candidate, item))));
Check("Нормовані оцінки належать [0; 1]", evaluations.All(x =>
    x.NormalizedPerformance is >= 0 and <= 1 && x.NormalizedCost is >= 0 and <= 1
    && x.NormalizedEfficiency is >= 0 and <= 1));
Check("Обрано об'єкт із максимальною функцією корисності",
    evaluations.First().Utility == evaluations.Max(x => x.Utility));

Console.WriteLine();
Console.WriteLine(failures.Count == 0
    ? "ПІДСУМОК: 9/9 перевірок виконано успішно."
    : $"ПІДСУМОК: помилок — {failures.Count}.");
return failures.Count == 0 ? 0 : 1;
