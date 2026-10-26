using SmashBattle.Domain.Clans;

namespace SmashBattle.Application.UseCases;

public sealed class ShowClanLeadersUseCase
{
    private readonly GameState _state;

    public ShowClanLeadersUseCase(GameState state) => _state = state;

    public void Execute()
    {
        Console.Clear();
        if (_state.LastBattle is null)
        {
            Console.WriteLine("Start a battle first to generate clan leaders.");
            Wait();
            return;
        }

        Console.WriteLine("SHOW CLAN LEADER");
        Console.WriteLine("1 - Dwargon\n2 - Elfis\n3 - Wrumper\n0 - Back");
        var clan = Console.ReadLine()?.Trim() switch
        {
            "1" => ClanType.Dwargon,
            "2" => ClanType.Elfis,
            "3" => ClanType.Wrumper,
            _ => (ClanType?)null
        };
        if (clan is null) return;
        var leader = _state.LastBattle.Clans.Single(item => item.Type == clan).Leader;
        Console.WriteLine($"\n{leader.Name} — Clan Leader of {leader.Clan}");
        Console.WriteLine($"Weapon: {leader.Weapon.Name}");
        Console.WriteLine($"HP: {leader.CurrentHealth}/{leader.BaseStats.MaximumHealth}");
        Console.WriteLine($"Damage: {leader.BaseStats.MinimumDamage}-{leader.BaseStats.MaximumDamage}");
        Console.WriteLine($"Aura: {leader.Aura!.Name}, radius {leader.Aura.Radius}");
        Wait();
    }

    private static void Wait()
    {
        Console.WriteLine("\nPress Enter to return.");
        Console.ReadLine();
    }
}
