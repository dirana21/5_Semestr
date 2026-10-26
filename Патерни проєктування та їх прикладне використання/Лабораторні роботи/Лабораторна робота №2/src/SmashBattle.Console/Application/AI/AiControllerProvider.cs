using SmashBattle.Domain.Clans;

namespace SmashBattle.Application.AI;

public sealed class AiControllerProvider
{
    private readonly IReadOnlyDictionary<ClanType, IAiController> _controllers;

    public AiControllerProvider(
        AggressiveAiController aggressive,
        RangedAiController ranged,
        DefensiveAiController defensive) =>
        _controllers = new Dictionary<ClanType, IAiController>
        {
            [ClanType.Wrumper] = aggressive,
            [ClanType.Elfis] = ranged,
            [ClanType.Dwargon] = defensive
        };

    public IAiController Get(ClanType clan) => _controllers[clan];
}
