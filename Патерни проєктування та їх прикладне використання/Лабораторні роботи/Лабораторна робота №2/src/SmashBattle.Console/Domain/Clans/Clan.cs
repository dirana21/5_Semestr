using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Battle;

namespace SmashBattle.Domain.Clans;

public sealed class Clan : IBattleComponent
{
    private readonly List<Combatant> _members;

    public Clan(ClanType type, IEnumerable<Combatant> members)
    {
        Type = type;
        _members = members.ToList();
    }

    public ClanType Type { get; }
    public IReadOnlyList<Combatant> Members => _members;
    public Combatant Leader => _members.Single(member => member.IsLeader);
    public bool IsAlive => _members.Any(member => member.IsAlive);
    public IEnumerable<Combatant> GetCombatants() => _members;
}
