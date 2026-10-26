using SmashBattle.Application.AI;
using SmashBattle.Application.Battle;
using SmashBattle.Application.Auras;
using SmashBattle.Application.Commands;
using SmashBattle.Application.Combat;
using SmashBattle.Application.Events;
using SmashBattle.Application.Logging;
using SmashBattle.Application.Movement;
using SmashBattle.Application.Persistence;
using SmashBattle.Application.Randomness;
using SmashBattle.Application.Stats;
using SmashBattle.Application.Turns;
using SmashBattle.Creation.Battle;
using SmashBattle.Creation.Clans;
using SmashBattle.Creation.Combatants;
using SmashBattle.Creation.Equipment;
using SmashBattle.Creation.Names;
using SmashBattle.Creation.World;
using SmashBattle.Domain.Clans;
using SmashBattle.Infrastructure.Persistence;
using SmashBattle.Infrastructure.Randomness;
using SmashBattle.Presentation.Controllers;
using SmashBattle.Presentation.Animation;
using SmashBattle.Presentation.Rendering;

namespace SmashBattle.Bootstrap;

public sealed class BattleRuntimeFactory
{
    private readonly string _savePath;

    public BattleRuntimeFactory(string savePath) => _savePath = savePath;

    public BattleRuntime Create(ClanType playerClan, int seed)
    {
        IRandomSource random = new SeededRandomSource(seed);
        var log = new BattleLog();
        var events = new BattleEventPublisher([log]);
        var terrain = new TerrainCatalog();
        var stats = new EffectiveStatsCalculator([new AuraStatsModifier(), new TerrainStatsModifier()]);
        var renderer = new ConsoleBattleRenderer(new ConsoleMapRenderer(terrain), new ConsoleHudRenderer(stats),
            new ConsoleBattleLogRenderer());
        var movementAnimation = new ConsoleMovementStepObserver(renderer, new MovementAnimationSettings(240));
        var movementCosts = new MovementCostCalculator(terrain);
        var reachable = new ReachableAreaFinder(movementCosts);
        var movement = new MovementService(events, movementAnimation);
        var damage = new DamagePipeline(new RollDamageStage(random), new CriticalDamageStage(random),
            new DefenseDamageStage(), new MinimumDamageStage());
        var combat = new CombatService(stats, damage, random, events);
        var abilities = new AbilityService(combat, events);
        var defend = new DefendService(events);

        var prototypes = new CombatantPrototypeCatalog();
        var names = new GeneratedNameProvider(random);
        var weapons = new WeaponCatalog();
        IClanFactory[] factories =
        [
            new ElfisClanFactory(prototypes, names, weapons, random),
            new DwargonClanFactory(prototypes, names, weapons, random),
            new WrumperClanFactory(prototypes, names, weapons, random)
        ];
        var builder = new BattleBuilder(new MapGenerator(random), new ClanFactoryProvider(factories));
        var battle = builder.Build(playerClan, seed);
        var auras = new AuraService();
        auras.Initialize(battle);
        var turns = new TurnScheduler(stats, events);
        var session = new BattleSession(battle, turns, log, reachable);
        movementAnimation.Attach(session);

        var commandDispatcher = new CommandDispatcher();
        var saveController = new BattleSaveController(new BattleMementoFactory(random), new BattleSaveStore(_savePath), events);
        var player = new PlayerTurnController(
            new PlayerMouseController(commandDispatcher, movement, combat, abilities, defend, renderer),
            new PlayerKeyboardController(commandDispatcher, movement, combat, abilities, saveController,
                new BattleLogViewer(), events));
        var ai = new AiControllerProvider(
            new AggressiveAiController(movement, combat, abilities, defend),
            new RangedAiController(movement, combat, abilities, defend),
            new DefensiveAiController(movement, combat, abilities, defend));
        var loop = new BattleLoop(renderer, player, ai, new VictoryCondition(), events, auras);
        return new BattleRuntime(session, loop);
    }
}
