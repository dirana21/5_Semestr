# Smash Battle

Turn-based console battle between three clans. The last clan with living characters wins.

## Mechanics

- The map is 50x50 cells with plains, forests, rocks, water and hills.
- Every character has health, damage, defense, speed, initiative, critical chance and dodge chance.
- Initiative determines the order of turns.
- Speed adds movement points at the beginning of a turn. Moving does not spend the main action.
- A character may move and then attack, use an ability or defend.
- The turn changes only after `END TURN` or `E` is pressed.
- Reachable cells are marked with a yellow `□`. Movement follows the calculated route one cell at a time.
- The HUD shows the active character, selected target and eight latest battle events. `L` opens the complete log.

## Clans

- **Elfis** - fast ranged fighters. Wind Aura increases speed and dodge chance. Ability: Arrow Rain.
- **Dwargon** - durable defensive fighters. Stone Aura increases defense and maximum health. Ability: Ground Slam.
- **Wrumper** - aggressive melee fighters. Rage Aura increases damage. Ability: Whirlwind.

The clan leader has 50% more health, 20% more damage and an aura with a radius of three cells. The aura does not affect its owner and disappears after the leader dies.

## Terrain

- Elfis receive a bonus in forests.
- Dwargon receive a bonus on rocks.
- Wrumper receive a bonus on plains.
- Hills improve ranged attacks.
- Water is impassable.

## Controls

- Mouse - select cells and HUD buttons.
- `WASD` or arrows - move one cell.
- `Tab` - select the next enemy.
- `Space` - attack mode.
- `Q` - unique ability mode.
- `E` - end turn.
- `X`, `Backspace`, right mouse button or `CANCEL` - cancel target selection.
- `P` - pause.
- `L` - complete battle log.
- `F5` / `F9` - save / load.
- `Esc` - cancel selection or return to the menu.

## Run

Open `SmashBattle.sln` in Visual Studio, select `SmashBattle.Console` as the startup project and press `Ctrl+F5`. The project requires .NET 9 and a console window of at least 100x32 characters. The seed is optional; press Enter to generate one automatically.
