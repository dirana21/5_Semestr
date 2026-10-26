using SmashBattle.Application.Events;
using SmashBattle.Application.Logging;
using SmashBattle.Application.Movement;
using SmashBattle.Creation.Combatants;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Common;
using SmashBattle.Domain.Equipment;

namespace SmashBattle.Tests.Movement;

public sealed class MovementServiceTests
{
    [Fact]
    public void Move_VisitsEveryPositionInTheCalculatedPath()
    {
        var start = new Position(0, 0);
        var firstStep = new Position(1, 0);
        var destination = new Position(2, 0);
        var actor = new CombatantPrototypeCatalog().Get(ClanType.Elfis)
            .Clone("Walker", new WeaponDefinition("Bow", 5, 0), start, false, 1);
        actor.BeginTurn(5m);
        var area = new ReachableArea(
            new Dictionary<Position, decimal> { [start] = 0, [firstStep] = 2.5m, [destination] = 5m },
            new Dictionary<Position, Position> { [firstStep] = start, [destination] = firstStep });
        var observer = new RecordingMovementStepObserver();
        var service = new MovementService(new BattleEventPublisher([new BattleLog()]), observer);

        var moved = service.Move(actor, destination, area);

        Assert.True(moved);
        Assert.Equal([firstStep, destination], observer.VisitedPositions);
        Assert.Equal(destination, actor.Position);
        Assert.Equal(0, actor.MovementPoints);
    }
}
