using PapaganCMS.Shared.DTOs.Onboarding;

namespace PapaganCMS.Core.Interfaces.Services;

public interface IOnboardingService
{
    Task<OnboardingProgressDto> GetProgressAsync(string userId);
    Task<OnboardingProgressDto> CompleteStepAsync(string userId, string step);
    Task<bool> SkipOnboardingAsync(string userId);
    Task<bool> SetupOrganizationAsync(string userId, OrganizationSetupDto dto);
    Task<bool> SetupFirstBotAsync(string userId, BotSetupDto dto);
}
