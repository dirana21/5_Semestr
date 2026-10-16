namespace DecisionTheoryLab3;

public sealed record ExpertRelation(int ExpertNumber, int[,] Matrix);

public sealed record CandidateResult(
    int ExpertNumber,
    int TotalDistance,
    int TotalSquaredDistance);

public sealed record KemenyAnalysis(
    int[,] DistanceMatrix,
    IReadOnlyList<CandidateResult> Candidates,
    IReadOnlyList<int> MedianExpertNumbers,
    IReadOnlyList<int> MeanExpertNumbers,
    int[,] ConsensusMatrix);

public static class Variant12Data
{
    public static IReadOnlyList<ExpertRelation> Create() =>
    [
        new(1, Matrix(
            "00111", "10010", "01001", "00100", "01010")),
        new(2, Matrix(
            "00111", "10010", "01001", "00100", "01010")),
        new(3, Matrix(
            "00111", "10010", "01001", "00100", "01010")),
        new(4, Matrix(
            "00101", "10010", "01001", "10100", "01010")),
        new(5, Matrix(
            "00101", "10010", "01000", "10100", "01110")),
        new(6, Matrix(
            "00111", "10010", "01000", "00100", "01110")),
        new(7, Matrix(
            "00101", "10010", "01001", "10100", "01010")),
        new(8, Matrix(
            "00101", "10010", "01001", "10100", "01010")),
        new(9, Matrix(
            "00101", "10010", "01011", "10000", "01010")),
        new(10, Matrix(
            "00000", "10010", "11001", "10100", "11010"))
    ];

    private static int[,] Matrix(params string[] rows)
    {
        var result = new int[rows.Length, rows.Length];
        for (var row = 0; row < rows.Length; row++)
        for (var column = 0; column < rows.Length; column++)
            result[row, column] = rows[row][column] - '0';
        return result;
    }
}
