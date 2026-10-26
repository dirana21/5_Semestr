using SmashBattle.Bootstrap;
using SmashBattle.Presentation.Menus;

namespace SmashBattle.Application.UseCases;

public sealed class StartBattleUseCase
{
    private readonly BattleSetupReader _setupReader;
    private readonly BattleRuntimeFactory _runtimeFactory;
    private readonly GameState _state;

    public StartBattleUseCase(BattleSetupReader setupReader, BattleRuntimeFactory runtimeFactory, GameState state)
    {
        _setupReader = setupReader;
        _runtimeFactory = runtimeFactory;
        _state = state;
    }

    public void Execute()
    {
        var setup = _setupReader.Read();
        var runtime = _runtimeFactory.Create(setup.PlayerClan, setup.Seed);
        _state.LastBattle = runtime.Session.Battle;
        runtime.Loop.Run(runtime.Session);
    }
}
