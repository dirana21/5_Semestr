using SmashBattle.Application.Battle;
using SmashBattle.Application.Movement;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;
using SmashBattle.Presentation.Rendering;

namespace SmashBattle.Presentation.Animation;

public sealed class ConsoleMovementStepObserver : IMovementStepObserver
{
    private readonly ConsoleBattleRenderer _renderer;
    private readonly MovementAnimationSettings _settings;
    private BattleSession? _session;

    public ConsoleMovementStepObserver(ConsoleBattleRenderer renderer, MovementAnimationSettings settings)
    {
        _renderer = renderer;
        _settings = settings;
    }

    public void Attach(BattleSession session) => _session = session;

    public void OnStep(Combatant actor, Position from, Position to, int stepNumber, int totalSteps)
    {
        if (_session is null) return;
        _session.RefreshReachableArea();
        _renderer.Render(_session);
        ConsoleCanvas.WriteAt(1, 20,
            $"Moving {actor.Name}: ({from.X},{from.Y}) -> ({to.X},{to.Y})  Step {stepNumber}/{totalSteps}".PadRight(96),
            ConsoleColor.Cyan);
        Thread.Sleep(_settings.StepDelayMilliseconds);
    }
}
