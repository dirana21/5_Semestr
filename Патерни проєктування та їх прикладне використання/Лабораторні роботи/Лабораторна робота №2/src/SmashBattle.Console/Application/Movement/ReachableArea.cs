using SmashBattle.Domain.Common;

namespace SmashBattle.Application.Movement;

public sealed class ReachableArea
{
    public ReachableArea(IReadOnlyDictionary<Position, decimal> costs, IReadOnlyDictionary<Position, Position> previous)
    {
        Costs = costs;
        Previous = previous;
    }

    public IReadOnlyDictionary<Position, decimal> Costs { get; }
    public IReadOnlyDictionary<Position, Position> Previous { get; }
    public bool Contains(Position position) => Costs.ContainsKey(position);

    public IReadOnlyList<Position> PathTo(Position target)
    {
        if (!Contains(target)) return [];
        var path = new List<Position> { target };
        while (Previous.TryGetValue(path[^1], out var previous)) path.Add(previous);
        path.Reverse();
        return path.Skip(1).ToList();
    }
}
