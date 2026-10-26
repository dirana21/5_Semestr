namespace SmashBattle.Domain.Common;

public readonly record struct Position(int X, int Y)
{
    public int ChebyshevDistanceTo(Position other) =>
        Math.Max(Math.Abs(X - other.X), Math.Abs(Y - other.Y));

    public IEnumerable<Position> Neighbors()
    {
        for (var y = -1; y <= 1; y++)
            for (var x = -1; x <= 1; x++)
                if (x != 0 || y != 0)
                    yield return new Position(X + x, Y + y);
    }
}
