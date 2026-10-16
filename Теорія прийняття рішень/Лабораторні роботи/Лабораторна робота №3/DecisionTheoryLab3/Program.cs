using DecisionTheoryLab3;
using System.Text;

Console.OutputEncoding = Encoding.UTF8;

var relations = Variant12Data.Create();
var analysis = KemenyAnalyzer.Analyze(relations);

Console.WriteLine("ТЕОРІЯ ПРИЙНЯТТЯ РІШЕНЬ — ЛАБОРАТОРНА РОБОТА № 3");
Console.WriteLine("Тема: обчислення медіани Кемені на бінарних відносинах");
Console.WriteLine($"Варіант 12 | {relations.Count} експертів | матриці 5 × 5\n");

Console.WriteLine("Матриця попарних відстаней Кемені:");
Console.Write("      ");
for (var i = 1; i <= relations.Count; i++) Console.Write($"{($"A{i}"),4}");
Console.WriteLine();
for (var row = 0; row < relations.Count; row++)
{
    Console.Write($"A{row + 1,-3} ");
    for (var column = 0; column < relations.Count; column++)
        Console.Write($"{analysis.DistanceMatrix[row, column],4}");
    Console.WriteLine();
}

Console.WriteLine("\nЦільові функції для кандидатів:");
Console.WriteLine("Експерт | ΣD  | ΣD²");
Console.WriteLine("--------+-----+-----");
foreach (var candidate in analysis.Candidates)
    Console.WriteLine($"A{candidate.ExpertNumber,-6} | {candidate.TotalDistance,3} | {candidate.TotalSquaredDistance,3}");

Console.WriteLine($"\nМедіана Кемені: A{string.Join(", A", analysis.MedianExpertNumbers)}; min ΣD = {analysis.Candidates.Min(x => x.TotalDistance)}");
Console.WriteLine($"Середнє за Кемені: A{string.Join(", A", analysis.MeanExpertNumbers)}; min ΣD² = {analysis.Candidates.Min(x => x.TotalSquaredDistance)}");
Console.WriteLine("Експерти 4, 7 і 8 подали однакову узгоджену матрицю.");

Console.WriteLine("\nПідсумкова матриця групового відношення:");
for (var row = 0; row < analysis.ConsensusMatrix.GetLength(0); row++)
{
    for (var column = 0; column < analysis.ConsensusMatrix.GetLength(1); column++)
        Console.Write($"{analysis.ConsensusMatrix[row, column]} ");
    Console.WriteLine();
}
