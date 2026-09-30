using System.Globalization;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using SolidShowcase.Core;

namespace SolidShowcase.Wpf;

public partial class MainWindow : Window
{
    private readonly DemoEnvironment _environment = new();

    public MainWindow()
    {
        InitializeComponent();
        ShowModule("import");
    }

    private void Module_Click(object sender, RoutedEventArgs e)
    {
        if (sender is Button { Tag: string moduleId })
        {
            ShowModule(moduleId);
        }
    }

    private void Action_Click(object sender, RoutedEventArgs e)
    {
        if (sender is not Button { Tag: string actionId }) return;
        ApplyResult(_environment.Execute(actionId));
    }

    private void TraceList_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (TraceList.SelectedItem is not SolidTraceStep step) return;
        TracePrinciple.Text = $"{step.Principle} · {step.Sequence:00}";
        TraceLocation.Text = step.Location;
        TraceExplanation.Text = $"{step.PrincipleName}. {step.Explanation}";
        CodePreview.Text = FormatCode(step.Code, step.HighlightedLine);
        TraceBadge.Background = PrincipleBrush(step.Principle);
    }

    private void ShowModule(string moduleId)
    {
        var module = _environment.Modules.First(item => item.Id == moduleId);
        ModuleEyebrow.Text = $"ЗАВДАННЯ {module.Number}";
        ModuleTitle.Text = module.Title;
        ModuleSubtitle.Text = module.Subtitle;
        ActionsList.ItemsSource = _environment.GetActions(moduleId);
        TraceList.ItemsSource = null;
        TracePrinciple.Text = "SOLID";
        TraceLocation.Text = "Оберіть дію";
        TraceExplanation.Text = "Тут з'явиться пояснення принципу SOLID і точка переходу в коді.";
        CodePreview.Text = "// Виконайте дію, щоб побачити код";
        ResultStatus.Text = "ГОТОВО";
        ImportForm.Visibility = moduleId == "import" ? Visibility.Visible : Visibility.Collapsed;
        LibraryForm.Visibility = moduleId == "library" ? Visibility.Visible : Visibility.Collapsed;
        FleetForm.Visibility = moduleId == "fleet" ? Visibility.Visible : Visibility.Collapsed;
        ManualTitle.Text = moduleId switch
        {
            "import" => "Імпортуйте власний файл",
            "library" => "Керуйте каталогом",
            _ => "Створіть власні дані автобази"
        };
        if (moduleId == "library") RefreshLibrarySelection();
        ShowResult(_environment.GetOverview(moduleId));
    }

    private void ShowResult(DemoResult result)
    {
        ResultTitle.Text = result.Title;
        ResultLines.ItemsSource = result.Lines;
    }

    private void ApplyResult(DemoResult result)
    {
        ShowResult(result);
        TraceList.ItemsSource = null;
        TraceList.ItemsSource = _environment.Trace;
        TraceList.SelectedIndex = _environment.Trace.Count > 0 ? 0 : -1;
        ResultStatus.Text = _environment.Trace.Count > 0 ? $"{_environment.Trace.Count} КРОКІВ" : "УВАГА";
    }

    private void FillImportSample_Click(object sender, RoutedEventArgs e)
    {
        ImportContentBox.Text = ComboText(ImportFormatCombo) == "JSON"
            ? "[{\"id\":\"11111111-1111-1111-1111-111111111111\",\"description\":\"Власна операція\",\"amount\":450.75}]"
            : "id,description,amount\n11111111-1111-1111-1111-111111111111,Власна операція,450.75";
    }

    private void ManualImport_Click(object sender, RoutedEventArgs e) =>
        ApplyResult(_environment.ImportCustom(ImportContentBox.Text, ComboText(ImportFormatCombo)));

    private LibraryItemDraft CreateLibraryDraft()
    {
        _ = int.TryParse(LibraryYearBox.Text, out var year);
        _ = int.TryParse(LibraryNumberBox.Text, out var number);
        return new LibraryItemDraft(
            ComboText(LibraryTypeCombo), LibraryTitleBox.Text, year, LibraryPublisherBox.Text,
            LibraryAuthorBox.Text, LibraryGenreBox.Text, number, number,
            DateOnly.TryParse(LibraryDateBox.Text, out var date) ? date : DateOnly.FromDateTime(DateTime.Today),
            LibraryDetailsBox.Text);
    }

    private void AddLibrary_Click(object sender, RoutedEventArgs e)
    {
        ApplyResult(_environment.AddLibraryItem(CreateLibraryDraft()));
        RefreshLibrarySelection();
        LibrarySelectionCombo.SelectedIndex = _environment.CatalogItems.Count - 1;
    }

    private void LoadLibrary_Click(object sender, RoutedEventArgs e)
    {
        if (LibrarySelectionCombo.SelectedItem is not LibraryItem item) return;
        LibraryTitleBox.Text = item.Title;
        LibraryPublisherBox.Text = item.Publisher;
        LibraryYearBox.Text = item.Year.ToString();
        LibraryTypeCombo.SelectedIndex = item switch { Newspaper => 1, Almanac => 2, _ => 0 };
        switch (item)
        {
            case Book book:
                LibraryAuthorBox.Text = book.Author; LibraryGenreBox.Text = book.Genre; LibraryNumberBox.Text = book.Pages.ToString();
                break;
            case Newspaper newspaper:
                LibraryNumberBox.Text = newspaper.IssueNumber.ToString(); LibraryDateBox.Text = newspaper.ReleaseDate.ToString("yyyy-MM-dd"); LibraryDetailsBox.Text = newspaper.Columns;
                break;
            case Almanac almanac:
                LibraryGenreBox.Text = almanac.Genre; LibraryDetailsBox.Text = string.Join(", ", almanac.Works);
                break;
        }
    }

    private void UpdateLibrary_Click(object sender, RoutedEventArgs e)
    {
        if (LibrarySelectionCombo.SelectedItem is not LibraryItem item) return;
        ApplyResult(_environment.UpdateLibraryItem(item.Id, CreateLibraryDraft()));
        RefreshLibrarySelection();
    }

    private void DeleteLibrary_Click(object sender, RoutedEventArgs e)
    {
        if (LibrarySelectionCombo.SelectedItem is not LibraryItem item) return;
        ApplyResult(_environment.RemoveLibraryItem(item.Id));
        RefreshLibrarySelection();
    }

    private void SearchLibrary_Click(object sender, RoutedEventArgs e) =>
        ApplyResult(_environment.SearchLibrary(ComboText(SearchFieldCombo), SearchQueryBox.Text));

    private void AddDriver_Click(object sender, RoutedEventArgs e)
    {
        _ = int.TryParse(DriverExperienceBox.Text, out var experience);
        ApplyResult(_environment.AddDriver(DriverNameBox.Text, experience));
    }

    private void AddVehicle_Click(object sender, RoutedEventArgs e)
    {
        _ = TryDecimal(VehicleCapacityBox.Text, out var capacity);
        _ = int.TryParse(VehicleDifficultyBox.Text, out var difficulty);
        ApplyResult(_environment.AddVehicle(VehicleModelBox.Text, capacity, difficulty));
    }

    private void DispatchCustom_Click(object sender, RoutedEventArgs e)
    {
        _ = TryDecimal(CargoWeightBox.Text, out var weight);
        _ = int.TryParse(DistanceBox.Text, out var distance);
        _ = int.TryParse(RequiredExperienceBox.Text, out var experience);
        ApplyResult(_environment.DispatchCustom(DestinationBox.Text, CargoTypeBox.Text, weight, distance, experience));
    }

    private void RefreshLibrarySelection()
    {
        LibrarySelectionCombo.ItemsSource = null;
        LibrarySelectionCombo.ItemsSource = _environment.CatalogItems;
    }

    private static string ComboText(ComboBox comboBox) =>
        comboBox.SelectedItem is ComboBoxItem item ? item.Content?.ToString() ?? string.Empty : string.Empty;

    private static bool TryDecimal(string text, out decimal value) =>
        decimal.TryParse(text, NumberStyles.Number, CultureInfo.CurrentCulture, out value) ||
        decimal.TryParse(text, NumberStyles.Number, CultureInfo.InvariantCulture, out value);

    private static string FormatCode(string code, int highlightedLine)
    {
        var lines = code.Replace("\r", string.Empty).Split('\n');
        return string.Join(Environment.NewLine, lines.Select((line, index) =>
            $"{(index + 1 == highlightedLine ? "▶" : " ")} {index + 1,2} │ {line}"));
    }

    private static Brush PrincipleBrush(SolidPrinciple principle) => principle switch
    {
        SolidPrinciple.S => new SolidColorBrush(Color.FromRgb(232, 115, 74)),
        SolidPrinciple.O => new SolidColorBrush(Color.FromRgb(65, 146, 136)),
        SolidPrinciple.L => new SolidColorBrush(Color.FromRgb(105, 122, 184)),
        SolidPrinciple.I => new SolidColorBrush(Color.FromRgb(194, 142, 58)),
        SolidPrinciple.D => new SolidColorBrush(Color.FromRgb(151, 92, 158)),
        _ => Brushes.Gray
    };
}
