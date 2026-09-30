using SolidShowcase.Core;

namespace SolidShowcase.Tests;

public sealed class SolidShowcaseTests
{
    [Fact]
    public void CsvPipeline_RejectsInvalidTransaction_AndWritesTrace()
    {
        var tracer = new SolidTracer();
        var repository = new InMemoryTransactionRepository(tracer);
        var content = $"id,description,amount\n{Guid.NewGuid()},Valid,100.50\n{Guid.NewGuid()},Invalid,-5";
        var processor = new ImportProcessor(
            new StringDataReader(content, tracer),
            new CsvTransactionParser(tracer),
            new PositiveAmountValidator(tracer),
            repository,
            new MemoryProgressReporter(tracer),
            new TextImportSummaryWriter(),
            tracer);

        var (result, _) = processor.Process();

        Assert.Equal(2, result.Total);
        Assert.Equal(1, result.Imported);
        Assert.Equal(1, result.Rejected);
        Assert.Single(repository.GetAll());
        Assert.Contains(tracer.Steps, step => step.Principle == SolidPrinciple.D);
        Assert.Contains(tracer.Steps, step => step.Principle == SolidPrinciple.O);
    }

    [Fact]
    public void Catalog_AcceptsAllPublicationTypes_ThroughBaseAbstraction()
    {
        var tracer = new SolidTracer();
        var repository = new InMemoryCatalogRepository();
        var service = new CatalogService(repository, new DemoLibraryItemFactory(tracer), tracer);

        service.Seed();

        Assert.Equal(3, service.Items.Count);
        Assert.Contains(service.Items, item => item is Book);
        Assert.Contains(service.Items, item => item is Newspaper);
        Assert.Contains(service.Items, item => item is Almanac);
        Assert.Contains(tracer.Steps, step => step.Principle == SolidPrinciple.L);
    }

    [Fact]
    public void Dispatch_ChoosesSmallestSuitableVehicle_AndExperiencedDriver()
    {
        var tracer = new SolidTracer();
        var repository = new InMemoryFleetRepository();
        var service = new DispatchService(
            repository,
            new ExperienceDriverSelectionStrategy(tracer),
            new BestFitVehicleSelectionStrategy(tracer),
            tracer);
        var request = new CargoRequest(Guid.NewGuid(), "Львів", "Обладнання", 6.2m, 540, 4);

        var trip = service.Dispatch(request);

        Assert.Equal("MAN TGL", trip.Vehicle.Model);
        Assert.Equal("Марія Коваль", trip.Driver.Name);
        Assert.False(trip.Vehicle.IsAvailable);
        Assert.False(trip.Driver.IsAvailable);
    }

    [Fact]
    public void CompletingTrip_ReleasesDriverAndVehicle_AndCalculatesPayment()
    {
        var tracer = new SolidTracer();
        var repository = new InMemoryFleetRepository();
        var service = new DispatchService(
            repository,
            new ExperienceDriverSelectionStrategy(tracer),
            new BestFitVehicleSelectionStrategy(tracer),
            tracer);
        var trip = service.Dispatch(new CargoRequest(Guid.NewGuid(), "Одеса", "Техніка", 2m, 100, 2));

        var payment = service.Complete(trip);

        Assert.True(trip.IsCompleted);
        Assert.True(trip.Driver.IsAvailable);
        Assert.True(trip.Vehicle.IsAvailable);
        Assert.Equal(650m, payment);
    }

    [Fact]
    public void ManualLibraryInput_CanBeAddedSearchedAndUpdated()
    {
        var environment = new DemoEnvironment();
        var draft = new LibraryItemDraft("Книга", "Архітектура коду", 2026, "Campus", "Олена", "Освіта", 320, 0, new DateOnly(2026, 1, 1), "");

        environment.AddLibraryItem(draft);
        var item = Assert.Single(environment.CatalogItems);
        var search = environment.SearchLibrary("Автор", "Олена");
        environment.UpdateLibraryItem(item.Id, draft with { Title = "SOLID на практиці" });

        Assert.Contains(search.Lines, line => line.Contains("Архітектура коду"));
        Assert.Equal("SOLID на практиці", environment.CatalogItems.Single().Title);
    }

    [Fact]
    public void ManualFleetInput_AddsResourcesAndDispatchesRequest()
    {
        var environment = new DemoEnvironment();

        environment.AddDriver("Тестовий водій", 12);
        environment.AddVehicle("Test Truck", 30m, 3);
        var result = environment.DispatchCustom("Харків", "Верстати", 25m, 700, 10);

        Assert.Contains(result.Lines, line => line.Contains("Test Truck") && line.Contains("у рейсі"));
        Assert.Contains(environment.Trace, step => step.Location == "DispatchService.Dispatch()");
    }
}
