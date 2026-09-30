namespace SolidShowcase.Core;

public sealed class ExperienceDriverSelectionStrategy(SolidTracer tracer) : IDriverSelectionStrategy
{
    public Driver Select(IReadOnlyCollection<Driver> drivers, CargoRequest request, Vehicle vehicle)
    {
        tracer.Add(
            "Автобаза",
            "Підбір водія",
            "ExperienceDriverSelectionStrategy.Select()",
            SolidPrinciple.O,
            "Open Closed Principle",
            "Правило призначення водія винесене у стратегію. Інший алгоритм можна додати без зміни DispatchService.",
            "return drivers\n    .Where(x => x.IsAvailable)\n    .Where(x => x.ExperienceYears >= required)\n    .OrderBy(x => x.ExperienceYears)\n    .First();",
            2);

        var required = Math.Max(request.RequiredExperience, vehicle.Difficulty / 2);
        return drivers
            .Where(driver => driver.IsAvailable && driver.ExperienceYears >= required)
            .OrderBy(driver => driver.ExperienceYears)
            .FirstOrDefault()
            ?? throw new InvalidOperationException("Немає доступного водія з необхідним стажем.");
    }
}
