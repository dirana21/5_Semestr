using System.Globalization;
using System.Text.Json;

namespace SolidShowcase.Core;

public sealed record LibraryItemDraft(
    string Kind,
    string Title,
    int Year,
    string Publisher,
    string Author,
    string Genre,
    int Pages,
    int IssueNumber,
    DateOnly ReleaseDate,
    string Details);

public sealed class DemoEnvironment
{
    private readonly SolidTracer _tracer = new();
    private readonly InMemoryCatalogRepository _catalogRepository = new();
    private readonly InMemoryFleetRepository _fleetRepository = new();
    private readonly CatalogService _catalog;
    private readonly DispatchService _dispatch;

    public DemoEnvironment()
    {
        _catalog = new CatalogService(_catalogRepository, new DemoLibraryItemFactory(_tracer), _tracer);
        _dispatch = new DispatchService(
            _fleetRepository,
            new ExperienceDriverSelectionStrategy(_tracer),
            new BestFitVehicleSelectionStrategy(_tracer),
            _tracer);
    }

    public IReadOnlyList<DemoModule> Modules { get; } =
    [
        new("import", "01", "Імпорт даних", "CSV / JSON → валідація → репозиторій → звіт"),
        new("library", "02", "Каталог бібліотеки", "Книги, газети й альманахи з пошуком"),
        new("fleet", "03", "Автобаза", "Заявки, водії, автомобілі, рейси та ремонт")
    ];

    public IReadOnlyList<SolidTraceStep> Trace => _tracer.Steps;
    public IReadOnlyList<LibraryItem> CatalogItems => _catalog.Items;
    public IReadOnlyList<Driver> Drivers => _fleetRepository.Drivers;
    public IReadOnlyList<Vehicle> Vehicles => _fleetRepository.Vehicles;

    public IReadOnlyList<DemoAction> GetActions(string moduleId) => moduleId switch
    {
        "import" =>
        [
            new("import.csv", "Імпортувати CSV", SolidPrinciple.O, "Пройти повний пайплайн із CSV-парсером"),
            new("import.json", "Імпортувати JSON", SolidPrinciple.D, "Замінити парсер без зміни ImportProcessor")
        ],
        "library" =>
        [
            new("library.seed", "Заповнити каталог", SolidPrinciple.S, "Створити тестові дані трьох типів"),
            new("library.add", "Додати випадкове", SolidPrinciple.O, "Фабрика повертає спільну абстракцію"),
            new("library.search", "Знайти «код»", SolidPrinciple.O, "Пошук через окрему стратегію"),
            new("library.remove", "Видалити останнє", SolidPrinciple.D, "Робота через інтерфейс репозиторію")
        ],
        "fleet" =>
        [
            new("fleet.dispatch", "Створити рейс", SolidPrinciple.D, "Підібрати водія й автомобіль стратегіями"),
            new("fleet.break", "Зімітувати поломку", SolidPrinciple.S, "Змінити стан автомобіля в активному рейсі"),
            new("fleet.complete", "Завершити рейс", SolidPrinciple.I, "Нарахувати виплату та звільнити ресурси"),
            new("fleet.repair", "Відремонтувати", SolidPrinciple.L, "Повернути автомобіль до доступного стану")
        ],
        _ => []
    };

    public DemoResult Execute(string actionId)
    {
        _tracer.Clear();
        try
        {
            return actionId switch
            {
                "import.csv" => RunImport(CreateCsv(), new CsvTransactionParser(_tracer), "CSV"),
                "import.json" => RunImport(CreateJson(), new JsonTransactionParser(_tracer), "JSON"),
                "library.seed" => SeedCatalog(),
                "library.add" => AddCatalogItem(),
                "library.search" => SearchCatalog(),
                "library.remove" => RemoveCatalogItem(),
                "fleet.dispatch" => DispatchTrip(),
                "fleet.break" => BreakVehicle(),
                "fleet.complete" => CompleteTrip(),
                "fleet.repair" => RepairVehicle(),
                _ => new DemoResult("Невідома дія", [actionId])
            };
        }
        catch (InvalidOperationException exception)
        {
            return new DemoResult("Операцію неможливо виконати", [exception.Message]);
        }
    }

    public DemoResult ImportCustom(string content, string format)
    {
        _tracer.Clear();
        if (string.IsNullOrWhiteSpace(content))
            return new DemoResult("Немає даних для імпорту", ["Вставте CSV або JSON у поле вводу."]);

        try
        {
            ITransactionParser parser = format.Equals("JSON", StringComparison.OrdinalIgnoreCase)
                ? new JsonTransactionParser(_tracer)
                : new CsvTransactionParser(_tracer);
            return RunImport(content, parser, format.ToUpperInvariant());
        }
        catch (Exception exception) when (exception is FormatException or JsonException)
        {
            return new DemoResult("Помилка формату", [exception.Message]);
        }
    }

    public DemoResult AddLibraryItem(LibraryItemDraft draft)
    {
        _tracer.Clear();
        if (string.IsNullOrWhiteSpace(draft.Title) || string.IsNullOrWhiteSpace(draft.Publisher))
            return new DemoResult("Заповніть обов'язкові поля", ["Назва і видавництво не можуть бути порожніми."]);

        var item = CreateLibraryItem(Guid.NewGuid(), draft);
        _catalog.Add(item);
        return CatalogSnapshot($"Додано: {item.Title}");
    }

    public DemoResult UpdateLibraryItem(Guid id, LibraryItemDraft draft)
    {
        _tracer.Clear();
        var updated = CreateLibraryItem(id, draft);
        var success = _catalog.Update(updated);
        return CatalogSnapshot(success ? $"Оновлено: {updated.Title}" : "Видання не знайдено");
    }

    public DemoResult RemoveLibraryItem(Guid id)
    {
        _tracer.Clear();
        var success = _catalog.Remove(id);
        return CatalogSnapshot(success ? "Видання видалено" : "Видання не знайдено");
    }

    public DemoResult SearchLibrary(string field, string query)
    {
        _tracer.Clear();
        if (string.IsNullOrWhiteSpace(query)) return CatalogSnapshot("Каталог бібліотеки");
        ILibrarySearchStrategy strategy = field switch
        {
            "Автор" => new AuthorSearchStrategy(),
            "Видавництво" => new PublisherSearchStrategy(),
            "Рік" => new YearSearchStrategy(),
            _ => new TitleSearchStrategy()
        };
        var items = _catalog.Search(strategy, query);
        return new DemoResult($"Пошук {strategy.Name}", items.Count == 0
            ? ["Нічого не знайдено"]
            : items.Select(FormatLibraryItem).ToList());
    }

    public DemoResult AddDriver(string name, int experienceYears)
    {
        _tracer.Clear();
        if (string.IsNullOrWhiteSpace(name) || experienceYears < 0)
            return new DemoResult("Некоректні дані водія", ["Вкажіть ім'я та невід'ємний стаж."]);
        var driver = new Driver(Guid.NewGuid(), name.Trim(), experienceYears);
        _fleetRepository.AddDriver(driver);
        _tracer.Add("Автобаза", $"Додано водія: {driver.Name}", "IFleetRepository.AddDriver()",
            SolidPrinciple.D, "Dependency Inversion Principle",
            "Інтерфейс користувача додає водія через контракт репозиторію, не працюючи з внутрішнім списком.",
            "_fleetRepository.AddDriver(new Driver(id, name, experience));", 1);
        return FleetSnapshot($"Водія {driver.Name} додано");
    }

    public DemoResult AddVehicle(string model, decimal capacityTons, int difficulty)
    {
        _tracer.Clear();
        if (string.IsNullOrWhiteSpace(model) || capacityTons <= 0 || difficulty < 1)
            return new DemoResult("Некоректні дані автомобіля", ["Вкажіть модель, додатну вантажопідйомність і складність."]);
        var vehicle = new Vehicle(Guid.NewGuid(), model.Trim(), capacityTons, difficulty);
        _fleetRepository.AddVehicle(vehicle);
        _tracer.Add("Автобаза", $"Додано автомобіль: {vehicle.Model}", "IFleetRepository.AddVehicle()",
            SolidPrinciple.D, "Dependency Inversion Principle",
            "Новий автомобіль передається репозиторію через абстракцію IFleetRepository.",
            "_fleetRepository.AddVehicle(new Vehicle(id, model, capacity, difficulty));", 1);
        return FleetSnapshot($"Автомобіль {vehicle.Model} додано");
    }

    public DemoResult DispatchCustom(string destination, string cargoType, decimal weightTons, int distanceKm, int requiredExperience)
    {
        _tracer.Clear();
        if (string.IsNullOrWhiteSpace(destination) || string.IsNullOrWhiteSpace(cargoType) || weightTons <= 0 || distanceKm <= 0)
            return new DemoResult("Некоректна заявка", ["Заповніть пункт призначення, тип вантажу, вагу та відстань."]);
        try
        {
            var request = new CargoRequest(Guid.NewGuid(), destination.Trim(), cargoType.Trim(), weightTons, distanceKm, requiredExperience);
            var trip = _dispatch.Dispatch(request);
            return FleetSnapshot($"Рейс створено: {trip.Driver.Name} → {trip.Vehicle.Model}");
        }
        catch (InvalidOperationException exception)
        {
            return new DemoResult("Рейс не створено", [exception.Message]);
        }
    }

    public DemoResult GetOverview(string moduleId) => moduleId switch
    {
        "import" => new DemoResult("Data Import Pipeline", [
            "Оберіть CSV або JSON, щоб побачити заміну парсера через інтерфейс.",
            "Праворуч з'явиться реальний ланцюжок викликів із поясненням SOLID."
        ]),
        "library" => CatalogSnapshot("Каталог бібліотеки"),
        "fleet" => FleetSnapshot("Стан автобази"),
        _ => new DemoResult("SOLID Showcase", ["Оберіть лабораторне завдання зліва."])
    };

    private DemoResult RunImport(string content, ITransactionParser parser, string format)
    {
        var repository = new InMemoryTransactionRepository(_tracer);
        var processor = new ImportProcessor(
            new StringDataReader(content, _tracer),
            parser,
            new PositiveAmountValidator(_tracer),
            repository,
            new MemoryProgressReporter(_tracer),
            new TextImportSummaryWriter(),
            _tracer);
        var (_, summary) = processor.Process();
        var lines = repository.GetAll()
            .Select(item => $"✓ {item.Description,-20} {item.Amount.ToString("0.00", CultureInfo.InvariantCulture)} ₴")
            .Prepend(summary)
            .ToList();
        return new DemoResult($"Імпорт {format} завершено", lines);
    }

    private DemoResult SeedCatalog()
    {
        _catalog.Seed();
        return CatalogSnapshot("Каталог ініціалізовано");
    }

    private DemoResult AddCatalogItem()
    {
        var item = _catalog.AddRandom();
        return CatalogSnapshot($"Додано: {item.Title}");
    }

    private DemoResult SearchCatalog()
    {
        _catalog.Seed();
        var items = _catalog.Search(new TitleSearchStrategy(), "код");
        return new DemoResult("Результат пошуку", items.Count == 0
            ? ["Нічого не знайдено"]
            : items.Select(FormatLibraryItem).ToList());
    }

    private DemoResult RemoveCatalogItem()
    {
        var removed = _catalog.RemoveLast();
        return CatalogSnapshot(removed ? "Останній об'єкт видалено" : "Каталог порожній");
    }

    private DemoResult CatalogSnapshot(string title)
    {
        var lines = _catalog.Items.Select(FormatLibraryItem).ToList();
        if (lines.Count == 0)
        {
            lines.Add("Каталог порожній. Натисніть «Заповнити каталог».");
        }
        return new DemoResult(title, lines);
    }

    private DemoResult DispatchTrip()
    {
        var request = new CargoRequest(Guid.NewGuid(), "Львів", "Обладнання", 6.2m, 540, 4);
        var trip = _dispatch.Dispatch(request);
        return FleetSnapshot($"Рейс створено: {trip.Driver.Name} → {trip.Vehicle.Model}");
    }

    private DemoResult BreakVehicle()
    {
        var trip = ActiveTrip() ?? throw new InvalidOperationException("Спочатку створіть рейс.");
        _dispatch.BreakVehicle(trip);
        return FleetSnapshot($"{trip.Vehicle.Model}: потрібен ремонт");
    }

    private DemoResult CompleteTrip()
    {
        var trip = ActiveTrip() ?? throw new InvalidOperationException("Немає активного рейсу.");
        var payment = _dispatch.Complete(trip);
        return FleetSnapshot($"Рейс завершено. Виплата: {payment:0.00} ₴");
    }

    private DemoResult RepairVehicle()
    {
        var vehicle = _fleetRepository.Vehicles.FirstOrDefault(item => item.NeedsRepair)
            ?? throw new InvalidOperationException("Немає автомобілів, що потребують ремонту.");
        _dispatch.Repair(vehicle);
        return FleetSnapshot($"{vehicle.Model} знову доступний");
    }

    private Trip? ActiveTrip() => _fleetRepository.Trips.LastOrDefault(trip => !trip.IsCompleted);

    private DemoResult FleetSnapshot(string title)
    {
        var lines = _fleetRepository.Vehicles.Select(vehicle =>
        {
            var state = vehicle.NeedsRepair ? "ремонт" : vehicle.IsAvailable ? "вільний" : "у рейсі";
            return $"{vehicle.Model,-20} {vehicle.CapacityTons,4:0.0} т · {state}";
        }).ToList();
        lines.AddRange(_fleetRepository.Drivers.Select(driver =>
            $"Водій: {driver.Name,-18} {driver.ExperienceYears} р. · {(driver.IsAvailable ? "вільний" : "у рейсі")}"));
        return new DemoResult(title, lines);
    }

    private static LibraryItem CreateLibraryItem(Guid id, LibraryItemDraft draft) => draft.Kind switch
    {
        "Газета" => new Newspaper(id, draft.Title.Trim(), draft.Year, draft.Publisher.Trim(),
            draft.IssueNumber, draft.ReleaseDate, draft.Details.Trim()),
        "Альманах" => new Almanac(id, draft.Title.Trim(), draft.Year, draft.Publisher.Trim(), draft.Genre.Trim(),
            draft.Details.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)),
        _ => new Book(id, draft.Title.Trim(), draft.Year, draft.Publisher.Trim(), draft.Author.Trim(),
            draft.Genre.Trim(), draft.Pages)
    };

    private static string FormatLibraryItem(LibraryItem item) =>
        $"{item.Kind,-9} · {item.Title} ({item.Year}) · {item.Details}";

    private static string CreateCsv() =>
        "id,description,amount\n" +
        $"{Guid.NewGuid()},Оплата навчання,2400.50\n" +
        $"{Guid.NewGuid()},Повернення,-40\n" +
        $"{Guid.NewGuid()},Канцелярія,315.20";

    private static string CreateJson() => JsonSerializer.Serialize(new[]
    {
        new Transaction(Guid.NewGuid(), "Підписка", 199.99m),
        new Transaction(Guid.NewGuid(), "Помилкова операція", -10m),
        new Transaction(Guid.NewGuid(), "Транспорт", 85.50m)
    });
}
