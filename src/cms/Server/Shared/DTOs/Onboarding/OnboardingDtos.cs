namespace SiteChatCMS.Shared.DTOs.Onboarding;

public class OnboardingProgressDto
{
    public string CurrentStep { get; set; } = "welcome";
    public List<string> CompletedSteps { get; set; } = new();
    public int TotalSteps { get; set; } = 4;
    public int ProgressPercentage => CompletedSteps.Count * 100 / TotalSteps;
}

public class CompleteStepDto
{
    public string Step { get; set; } = string.Empty;
}

public class OrganizationSetupDto
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? Website { get; set; }
}

public class BotSetupDto
{
    public string Name { get; set; } = string.Empty;
    public string? SiteUrl { get; set; }
    public string? Description { get; set; }
    public string? Purpose { get; set; }
}
