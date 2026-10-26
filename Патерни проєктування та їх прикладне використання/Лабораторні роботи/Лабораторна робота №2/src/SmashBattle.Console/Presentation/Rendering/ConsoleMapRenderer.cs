using SmashBattle.Application.Battle;
using SmashBattle.Creation.World;
using SmashBattle.Domain.Common;

namespace SmashBattle.Presentation.Rendering;

public sealed class ConsoleMapRenderer
{
    private readonly TerrainCatalog _terrain;

    public ConsoleMapRenderer(TerrainCatalog terrain) => _terrain = terrain;

    public Viewport CurrentViewport { get; private set; } =
        new(0, 0, ConsoleLayout.MapWidth, ConsoleLayout.MapHeight);

    public void Render(BattleSession session)
    {
        CurrentViewport = CenterOn(session.CurrentActor.Position, session.Battle.Map.Width, session.Battle.Map.Height);
        var auraCells = AuraCells(session);
        var enemies = session.Battle.LivingCombatants.Where(actor => actor.Clan != session.CurrentActor.Clan).ToList();

        for (var screenY = 0; screenY < ConsoleLayout.MapHeight; screenY++)
            for (var screenX = 0; screenX < ConsoleLayout.MapWidth; screenX++)
            {
                var world = new Position(CurrentViewport.Left + screenX, CurrentViewport.Top + screenY);
                var actor = session.Battle.LivingCombatants.FirstOrDefault(item => item.Position == world);
                var terrain = _terrain.Get(session.Battle.Map.TerrainAt(world));
                var symbol = actor?.Symbol ?? terrain.Symbol;
                var foreground = actor is null ? ConsolePalette.ForTerrain(terrain.Type) : ConsolePalette.ForClan(actor.Clan);
                var background = ConsoleColor.Black;
                if (actor is null && auraCells.Contains(world))
                {
                    symbol = '·';
                    foreground = ConsoleColor.DarkGreen;
                }
                if (actor is null && session.Mode == InteractionMode.Move && session.ReachableArea.Contains(world))
                {
                    symbol = '□';
                    foreground = ConsoleColor.Yellow;
                }
                if (session.Mode == InteractionMode.Attack && enemies.Any(enemy => enemy.Position == world &&
                        session.CurrentActor.Position.ChebyshevDistanceTo(world) <= session.CurrentActor.Weapon.Range))
                    foreground = ConsoleColor.White;
                if (session.Mode == InteractionMode.Ability &&
                    session.CurrentActor.Position.ChebyshevDistanceTo(world) <= session.CurrentActor.Ability.Range)
                {
                    if (actor is null) symbol = '◇';
                    foreground = ConsoleColor.Magenta;
                }
                if (actor?.Id == session.CurrentActor.Id) background = ConsoleColor.DarkGray;
                ConsoleCanvas.WriteCell(ConsoleLayout.MapLeft + screenX, ConsoleLayout.MapTop + screenY,
                    symbol, foreground, background);
            }
    }

    public Position? ScreenToWorld(int x, int y)
    {
        if (x < ConsoleLayout.MapLeft || x >= ConsoleLayout.MapLeft + ConsoleLayout.MapWidth ||
            y < ConsoleLayout.MapTop || y >= ConsoleLayout.MapTop + ConsoleLayout.MapHeight) return null;
        return new Position(CurrentViewport.Left + x - ConsoleLayout.MapLeft,
            CurrentViewport.Top + y - ConsoleLayout.MapTop);
    }

    private static Viewport CenterOn(Position focus, int mapWidth, int mapHeight) => new(
        Math.Clamp(focus.X - ConsoleLayout.MapWidth / 2, 0, mapWidth - ConsoleLayout.MapWidth),
        Math.Clamp(focus.Y - ConsoleLayout.MapHeight / 2, 0, mapHeight - ConsoleLayout.MapHeight),
        ConsoleLayout.MapWidth,
        ConsoleLayout.MapHeight);

    private static HashSet<Position> AuraCells(BattleSession session) => session.Battle.Clans
        .Select(clan => clan.Leader)
        .Where(leader => leader.IsAlive && leader.Aura is not null)
        .SelectMany(leader => PositionsInRadius(leader.Position, leader.Aura!.Radius))
        .Where(session.Battle.Map.Contains)
        .ToHashSet();

    private static IEnumerable<Position> PositionsInRadius(Position center, int radius)
    {
        for (var y = center.Y - radius; y <= center.Y + radius; y++)
            for (var x = center.X - radius; x <= center.X + radius; x++)
            {
                var position = new Position(x, y);
                if (center.ChebyshevDistanceTo(position) <= radius) yield return position;
            }
    }
}
