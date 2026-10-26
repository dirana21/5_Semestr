# Architecture

The application follows dependency direction from the outside toward the domain:

```text
Presentation ─┐
Infrastructure├──> Application ───> Domain
Creation ─────┘
       Bootstrap only wires concrete objects
```

## Responsibilities

### Domain

Contains state, not workflows. `Combatant` owns health, position, cooldown and state transitions. `BattleState` owns the map and clans. `BattleMap` exposes terrain without knowing how it is rendered.

### Creation

Builds complete object graphs. `CombatantPrototypeCatalog` stores race templates. Three concrete subclasses of `ClanFactoryBase` clone them. `BattleBuilder` creates the map, spawn blocks and three clans. Catalogs reuse immutable weapon and terrain values.

### Application

Contains use cases and game rules. Each area is isolated:

- `Movement` calculates terrain cost and reachable cells.
- `Combat` resolves attacks, abilities, defense and damage stages.
- `Stats` layers aura and terrain modifiers.
- `Turns` controls initiative order.
- `AI` contains one replaceable policy per clan.
- `Commands` wraps every player action.
- `Events` and `Logging` keep the UI independent from battle events.
- `Persistence` captures and restores a memento.

### Infrastructure

Contains technology-specific implementations: deterministic random source, JSON files, standard console keyboard input and Win32 mouse input.

### Presentation

`ConsoleBattleRenderer` draws the viewport and HUD. `PlayerTurnController` translates keys/clicks into commands. It never calculates damage or movement costs.

### Bootstrap

`GameCompositionRoot` creates the main menu. `BattleRuntimeFactory` wires one battle runtime. Neither contains game rules.
