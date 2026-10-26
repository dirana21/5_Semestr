# Pattern map

| Pattern | Main implementation | Why it exists |
|---|---|---|
| Abstract Factory | `IClanFactory`, three concrete clan factories, `ClanFactoryProvider` | The builder requests a clan family by abstraction. |
| Factory Method | `ClanFactoryBase.CreatePrototype` | Each concrete factory overrides the method that supplies its race prototype. |
| Prototype | `CombatantPrototype.Clone` | Configured race templates are copied into unique fighters. |
| Builder | `BattleBuilder` | A 50×50 map, spawn zones, clans and leaders are assembled in a defined sequence. |
| Singleton | `ClanLeadershipRegistry` | There is one registry with exactly one current leader slot per clan. |
| Adapter | `WindowsConsoleInputReader` | Native Win32 records become application-level `GameInput`. |
| Decorator | `IStatsModifier` pipeline | Aura and terrain bonuses layer over base stats without changing `Combatant`. |
| Flyweight | `WeaponCatalog`, `TerrainCatalog` | Immutable definitions are shared by many cells and fighters. |
| Bridge | `BattleMap` + `ConsoleBattleRenderer` | Map storage and console visualization can evolve separately. |
| Composite | `IBattleComponent`, `BattleState`, `Clan`, `Combatant` | A battle tree and a single fighter can be traversed through the same contract. |
| Command | `IPlayerCommand` implementations | Mouse and keyboard invoke the same testable actions. |
| Strategy | AI controller classes and stat/movement policies | Clan behavior is selected at runtime. |
| State | `CombatantState` | Idle, moving, attacking, defending, stunned and dead are explicit. |
| Observer | `BattleEventPublisher`, `BattleLog` | Combat rules publish events without depending on HUD or file output. |
| Chain of Responsibility | `DamageStage` chain | Roll, critical, defense and minimum damage are separate stages. |
| Template Method | `AiTurnTemplate` | All AI turns use one algorithm with clan-specific target/position hooks. |
| Memento | `BattleMemento`, `BattleMementoFactory` | F5/F9 stores and restores battle state without exposing save logic to entities. |

Patterns are placed around real variation points. Adding a new terrain modifier, damage stage, AI policy or event subscriber does not require editing the unrelated subsystems.
