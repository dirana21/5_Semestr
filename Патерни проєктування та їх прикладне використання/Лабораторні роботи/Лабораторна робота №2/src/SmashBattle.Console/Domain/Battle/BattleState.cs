using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.World;

namespace SmashBattle.Domain.Battle;

public sealed class BattleState : IBattleComponent
{
    public BattleState(BattleMap map, IReadOnlyList<Clan> clans, ClanType playerClan, int seed)
    {
        Map = map;
        Clans = clans;
        PlayerClan = playerClan;
        Seed = seed;
    }

    public BattleMap Map { get; }
    public IReadOnlyList<Clan> Clans { get; }
    public ClanType PlayerClan { get; }
    public int Seed { get; }
    public int Round { get; set; } = 1;
    public int TurnIndex { get; set; }
    public IReadOnlyList<Combatant> LivingCombatants =>
        Clans.SelectMany(clan => clan.Members).Where(member => member.IsAlive).ToList();
    public IEnumerable<Combatant> GetCombatants() => Clans.SelectMany(clan => clan.GetCombatants());
}
