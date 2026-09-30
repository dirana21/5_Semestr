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
        var result = _environment.Execute(actionId);
        ShowResult(result);
        TraceList.ItemsSource = _environment.Trace;
        TraceList.SelectedIndex = _environment.Trace.Count > 0 ? 0 : -1;
        ResultStatus.Text = _environment.Trace.Count > 0 ? $"{_environment.Trace.Count} КРОКІВ" : "УВАГА";
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
        ShowResult(_environment.GetOverview(moduleId));
    }

    private void ShowResult(DemoResult result)
    {
        ResultTitle.Text = result.Title;
        ResultLines.ItemsSource = result.Lines;
    }

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
