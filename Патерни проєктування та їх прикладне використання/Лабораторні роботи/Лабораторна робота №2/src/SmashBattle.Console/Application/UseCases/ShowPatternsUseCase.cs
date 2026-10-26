namespace SmashBattle.Application.UseCases;

public sealed class ShowPatternsUseCase
{
    private static readonly string[] Patterns =
    [
        "CREATIONAL",
        "Abstract Factory — creates complete clan families through IClanFactory.",
        "Factory Method — selects weapons, abilities and race-specific prototypes.",
        "Prototype — clones configured CombatantPrototype objects.",
        "Builder — BattleBuilder assembles map, clans and leaders step by step.",
        "Singleton — ClanLeadershipRegistry owns one leader slot per clan.",
        "",
        "STRUCTURAL",
        "Adapter — WindowsConsoleInputReader converts Win32 input into GameInput.",
        "Decorator — IStatsModifier layers aura and terrain bonuses.",
        "Flyweight — weapon and terrain definitions are shared catalog values.",
        "Bridge — BattleMap data is independent from ConsoleBattleRenderer.",
        "Composite — IBattleComponent represents BattleState, Clan and Combatant uniformly.",
        "",
        "BEHAVIORAL",
        "Command — each player action is an IPlayerCommand.",
        "Strategy — three AI controllers and movement/target policies are replaceable.",
        "State — CombatantState controls idle, moving, attacking, defending and stunned behavior.",
        "Observer — BattleEventPublisher sends events to the full BattleLog.",
        "Chain of Responsibility — damage passes through roll, critical, defense and minimum stages.",
        "Template Method — AiTurnTemplate defines the common AI turn sequence.",
        "Memento — F5 captures and F9 restores BattleMemento, including random state."
    ];

    public void Execute()
    {
        Console.Clear();
        Console.WriteLine("PATTERNS USED IN SMASH BATTLE\n");
        foreach (var line in Patterns) Console.WriteLine(line);
        Console.WriteLine("\nPress Enter to return.");
        Console.ReadLine();
    }
}
