using System.Text.Json;
using SmashBattle.Application.Persistence;

namespace SmashBattle.Infrastructure.Persistence;

public sealed class BattleSaveStore
{
    private readonly string _filePath;
    private readonly JsonSerializerOptions _options = new() { WriteIndented = true };

    public BattleSaveStore(string filePath) => _filePath = filePath;

    public void Save(BattleMemento memento)
    {
        var directory = Path.GetDirectoryName(_filePath);
        if (!string.IsNullOrEmpty(directory)) Directory.CreateDirectory(directory);
        File.WriteAllText(_filePath, JsonSerializer.Serialize(memento, _options));
    }

    public BattleMemento? Load() => File.Exists(_filePath)
        ? JsonSerializer.Deserialize<BattleMemento>(File.ReadAllText(_filePath), _options)
        : null;
}
