using SmashBattle.Application.Movement;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;

namespace SmashBattle.Tests.Movement;

internal sealed class RecordingMovementStepObserver : IMovementStepObserver
{
    public List<Position> VisitedPositions { get; } = [];

    public void OnStep(Combatant actor, Position from, Position to, int stepNumber, int totalSteps) =>
        VisitedPositions.Add(to);
}
