namespace SmashBattle.Application.UseCases;

public sealed class ShowClanCompositionUseCase
{
    private readonly GameState _state;

    public ShowClanCompositionUseCase(GameState state) => _state = state;

    public void Execute()
    {
        Console.Clear();
        Console.WriteLine("CLAN COMPOSITION");
        if (_state.LastBattle is null)
            Console.WriteLine("Start a battle first to generate deterministic clan members.");
        else
            foreach (var clan in _state.LastBattle.Clans)
            {
                Console.WriteLine($"\n{clan.Type} ({clan.Members.Count} members)");
                foreach (var actor in clan.Members)
                    Console.WriteLine($"- {actor.Name}{(actor.IsLeader ? " [CLAN LEADER]" : "")} | " +
                                      $"{actor.Weapon.Name} | HP {actor.CurrentHealth}/{actor.BaseStats.MaximumHealth} | " +
                                      $"DMG {actor.BaseStats.MinimumDamage}-{actor.BaseStats.MaximumDamage} | " +
                                      $"DEF {actor.BaseStats.Defense} | SPD {actor.BaseStats.Speed}");
            }
        Wait();
    }

    private static void Wait()
    {
        Console.WriteLine("\nPress Enter to return.");
        Console.ReadLine();
    }
}
