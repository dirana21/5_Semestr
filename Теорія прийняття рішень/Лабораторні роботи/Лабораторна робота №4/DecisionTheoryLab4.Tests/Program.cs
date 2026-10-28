using DecisionTheoryLab4;
using System.Text;

Console.OutputEncoding = Encoding.UTF8;

var three = Variant12Data.AnalyzeThreePointScale();
var nine = Variant12Data.AnalyzeNinePointScale();
var passed = 0;

Check("Матриця критеріїв трибальної шкали обернено симетрична", IsValid(Variant12Data.GetThreePointCriteriaMatrix()));
Check("Матриця критеріїв дев'ятибальної шкали обернено симетрична", IsValid(Variant12Data.GetNinePointCriteriaMatrix()));
Check("Сума ваг критеріїв трибальної шкали дорівнює 1", Near(three.Criteria.Priorities.Sum(), 1));
Check("Сума ваг критеріїв дев'ятибальної шкали дорівнює 1", Near(nine.Criteria.Priorities.Sum(), 1));
Check("Ваги критеріїв трибальної шкали правильні", SequenceNear(three.Criteria.Priorities, [0.539615, 0.163424, 0.296961]));
Check("Ваги критеріїв дев'ятибальної шкали правильні", SequenceNear(nine.Criteria.Priorities, [0.636986, 0.104729, 0.258285]));
Check("Усі матриці трибальної шкали узгоджені", AllConsistent(three));
Check("Усі матриці дев'ятибальної шкали узгоджені", AllConsistent(nine));
Check("Глобальні пріоритети трибальної шкали правильні", SequenceNear(three.GlobalPriorities, [0.336617, 0.296961, 0.366422]));
Check("Глобальні пріоритети дев'ятибальної шкали правильні", SequenceNear(nine.GlobalPriorities, [0.297946, 0.258285, 0.443769]));
Check("Сума глобальних пріоритетів трибальної шкали дорівнює 1", Near(three.GlobalPriorities.Sum(), 1));
Check("Сума глобальних пріоритетів дев'ятибальної шкали дорівнює 1", Near(nine.GlobalPriorities.Sum(), 1));
Check("За трибальною шкалою обрано Молодіжне", three.BestAlternativeIndex == 2);
Check("За дев'ятибальною шкалою обрано Молодіжне", nine.BestAlternativeIndex == 2);
Check("Обидві шкали дали однакове рішення", three.BestAlternativeIndex == nine.BestAlternativeIndex);

Console.WriteLine($"\nПІДСУМОК: {passed}/15 перевірок виконано успішно.");
return passed == 15 ? 0 : 1;

void Check(string name, bool condition)
{
    Console.WriteLine($"[{(condition ? "PASS" : "FAIL")}] {name}");
    if (condition) passed++;
}

static bool IsValid(double[,] matrix)
{
    try
    {
        AhpAnalyzer.Validate(matrix);
        return true;
    }
    catch (ArgumentException)
    {
        return false;
    }
}

static bool Near(double actual, double expected, double tolerance = 1e-5) => Math.Abs(actual - expected) <= tolerance;

static bool SequenceNear(IReadOnlyList<double> actual, IReadOnlyList<double> expected) =>
    actual.Count == expected.Count && actual.Select((value, index) => Near(value, expected[index])).All(value => value);

static bool AllConsistent(ScaleAnalysis analysis) =>
    analysis.Criteria.IsConsistent && analysis.AlternativesByCriterion.All(result => result.IsConsistent);
