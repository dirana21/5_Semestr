using SmashBattle.Application;
using SmashBattle.Application.UseCases;
using SmashBattle.Domain.Clans;
using SmashBattle.Infrastructure.Randomness;
using SmashBattle.Presentation.Menus;

namespace SmashBattle.Bootstrap;

public static class GameCompositionRoot
{
    public static MainMenu Create()
    {
        var state = new GameState();
        var savePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "SmashBattle", "battle-save.json");
        var runtimeFactory = new BattleRuntimeFactory(savePath);
        state.LastBattle = runtimeFactory.Create(ClanType.Elfis, 0).Session.Battle;
        return new MainMenu(
            new StartBattleUseCase(new BattleSetupReader(new RandomSeedGenerator()), runtimeFactory, state),
            new ShowClanCompositionUseCase(state),
            new ShowClanLeadersUseCase(state),
            new ShowPatternsUseCase());
    }
}
