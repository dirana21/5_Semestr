using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.Movement;

public sealed class ReachableAreaFinder
{
    private readonly MovementCostCalculator _costs;

    public ReachableAreaFinder(MovementCostCalculator costs) => _costs = costs;

    public ReachableArea Find(BattleState battle, Combatant actor)
    {
        var occupied = battle.LivingCombatants.Where(item => item.Id != actor.Id).Select(item => item.Position).ToHashSet();
        var distances = new Dictionary<Position, decimal> { [actor.Position] = 0 };
        var previous = new Dictionary<Position, Position>();
        var queue = new PriorityQueue<Position, decimal>();
        queue.Enqueue(actor.Position, 0);

        while (queue.TryDequeue(out var current, out var currentCost))
        {
            if (currentCost > distances[current]) continue;
            foreach (var neighbor in current.Neighbors())
            {
                if (!battle.Map.Contains(neighbor) || occupied.Contains(neighbor)) continue;
                var terrain = battle.Map.TerrainAt(neighbor);
                if (!_costs.IsPassable(terrain)) continue;
                var nextCost = currentCost + _costs.GetCost(actor, terrain);
                if (nextCost > actor.MovementPoints ||
                    distances.TryGetValue(neighbor, out var known) && known <= nextCost) continue;
                distances[neighbor] = nextCost;
                previous[neighbor] = current;
                queue.Enqueue(neighbor, nextCost);
            }
        }

        return new ReachableArea(distances, previous);
    }
}
