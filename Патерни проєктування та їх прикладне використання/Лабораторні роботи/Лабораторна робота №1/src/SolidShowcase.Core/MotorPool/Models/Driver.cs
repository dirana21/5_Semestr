namespace SolidShowcase.Core;

public sealed class Driver(Guid id, string name, int experienceYears)
{
    public Guid Id { get; } = id;
    public string Name { get; } = name;
    public int ExperienceYears { get; } = experienceYears;
    public bool IsAvailable { get; set; } = true;
}
