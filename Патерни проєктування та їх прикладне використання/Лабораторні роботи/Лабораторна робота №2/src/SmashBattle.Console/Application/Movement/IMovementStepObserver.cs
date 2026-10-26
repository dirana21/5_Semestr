using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.Movement;

public interface IMovementStepObserver
{
    void OnStep(Combatant actor, Position from, Position to, int stepNumber, int totalSteps);
}
