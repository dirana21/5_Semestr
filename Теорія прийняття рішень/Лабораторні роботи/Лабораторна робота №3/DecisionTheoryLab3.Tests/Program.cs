using DecisionTheoryLab3;
using System.Text;

Console.OutputEncoding = Encoding.UTF8;

var relations = Variant12Data.Create();
var analysis = KemenyAnalyzer.Analyze(relations);
var passed = 0;

Check("Завантажено 10 експертних матриць", relations.Count == 10);
Check("Усі матриці мають розмір 5 × 5", relations.All(x => x.Matrix.GetLength(0) == 5 && x.Matrix.GetLength(1) == 5));
Check("Усі матриці є коректними бінарними відношеннями", ValidateAll(relations));
Check("Матриця відстаней симетрична", IsSymmetric(analysis.DistanceMatrix));
Check("На діагоналі матриці відстаней стоять нулі", HasZeroDiagonal(analysis.DistanceMatrix));
Check("Перший рядок відстаней дорівнює 0, 0, 0, 2, 4, 2, 2, 2, 4, 6", RowEquals(analysis.DistanceMatrix, 0, [0, 0, 0, 2, 4, 2, 2, 2, 4, 6]));
Check("Суми відстаней дорівнюють 22, 22, 22, 18, 30, 34, 18, 18, 34, 50", analysis.Candidates.Select(x => x.TotalDistance).SequenceEqual([22, 22, 22, 18, 30, 34, 18, 18, 34, 50]));
Check("Суми квадратів відстаней дорівнюють 84, 84, 84, 52, 116, 164, 52, 52, 148, 292", analysis.Candidates.Select(x => x.TotalSquaredDistance).SequenceEqual([84, 84, 84, 52, 116, 164, 52, 52, 148, 292]));
Check("Медіану Кемені задають експерти 4, 7 і 8", analysis.MedianExpertNumbers.SequenceEqual([4, 7, 8]));
Check("Середнє за Кемені задають експерти 4, 7 і 8", analysis.MeanExpertNumbers.SequenceEqual([4, 7, 8]));
Check("Мінімальна сума відстаней дорівнює 18", analysis.Candidates.Min(x => x.TotalDistance) == 18);
Check("Мінімальна сума квадратів відстаней дорівнює 52", analysis.Candidates.Min(x => x.TotalSquaredDistance) == 52);
Check("Матриці експертів 4, 7 і 8 однакові", KemenyAnalyzer.KemenyDistance(relations[3].Matrix, relations[6].Matrix) == 0 && KemenyAnalyzer.KemenyDistance(relations[3].Matrix, relations[7].Matrix) == 0);

Console.WriteLine($"\nПІДСУМОК: {passed}/13 перевірок виконано успішно.");
return passed == 13 ? 0 : 1;

void Check(string name, bool condition)
{
    Console.WriteLine($"[{(condition ? "PASS" : "FAIL")}] {name}");
    if (condition) passed++;
}

static bool ValidateAll(IEnumerable<ExpertRelation> values)
{
    try
    {
        foreach (var value in values) KemenyAnalyzer.ValidateBinaryRelation(value.Matrix);
        return true;
    }
    catch (ArgumentException)
    {
        return false;
    }
}

static bool IsSymmetric(int[,] matrix)
{
    for (var row = 0; row < matrix.GetLength(0); row++)
    for (var column = 0; column < matrix.GetLength(1); column++)
        if (matrix[row, column] != matrix[column, row]) return false;
    return true;
}

static bool HasZeroDiagonal(int[,] matrix)
{
    for (var index = 0; index < matrix.GetLength(0); index++)
        if (matrix[index, index] != 0) return false;
    return true;
}

static bool RowEquals(int[,] matrix, int row, IReadOnlyList<int> expected)
{
    for (var column = 0; column < matrix.GetLength(1); column++)
        if (matrix[row, column] != expected[column]) return false;
    return true;
}
