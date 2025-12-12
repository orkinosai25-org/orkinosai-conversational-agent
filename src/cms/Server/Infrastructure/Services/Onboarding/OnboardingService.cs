using Microsoft.EntityFrameworkCore;
using PapaganCMS.Core.Entities.Identity;
using PapaganCMS.Core.Interfaces.Services;
using PapaganCMS.Infrastructure.Data;
using PapaganCMS.Shared.DTOs.Onboarding;

namespace PapaganCMS.Infrastructure.Services.Onboarding;

public class OnboardingService : IOnboardingService
{
    private readonly ApplicationDbContext _context;
    private static readonly List<string> OnboardingSteps = new() { "welcome", "organization", "bot", "complete" };

    public OnboardingService(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<OnboardingProgressDto> GetProgressAsync(string userId)
    {
        var user = await _context.Users.FindAsync(userId);
        if (user == null)
        {
            throw new InvalidOperationException("User not found");
        }

        var currentStep = user.OnboardingStep ?? "welcome";
        var currentStepIndex = OnboardingSteps.IndexOf(currentStep);
        var completedSteps = currentStepIndex >= 0
            ? OnboardingSteps.Take(currentStepIndex).ToList()
            : new List<string>();

        return new OnboardingProgressDto
        {
            CurrentStep = currentStep,
            CompletedSteps = completedSteps,
            TotalSteps = OnboardingSteps.Count
        };
    }

    public async Task<OnboardingProgressDto> CompleteStepAsync(string userId, string step)
    {
        var user = await _context.Users.FindAsync(userId);
        if (user == null)
        {
            throw new InvalidOperationException("User not found");
        }

        var stepIndex = OnboardingSteps.IndexOf(step);
        if (stepIndex == -1)
        {
            throw new ArgumentException("Invalid onboarding step", nameof(step));
        }

        // Move to next step
        if (stepIndex < OnboardingSteps.Count - 1)
        {
            user.OnboardingStep = OnboardingSteps[stepIndex + 1];
        }
        else
        {
            user.OnboardingStep = "complete";
            user.HasCompletedOnboarding = true;
        }

        await _context.SaveChangesAsync();

        return await GetProgressAsync(userId);
    }

    public async Task<bool> SkipOnboardingAsync(string userId)
    {
        var user = await _context.Users.FindAsync(userId);
        if (user == null)
        {
            return false;
        }

        user.HasCompletedOnboarding = true;
        user.OnboardingStep = "complete";
        await _context.SaveChangesAsync();

        return true;
    }

    public async Task<bool> SetupOrganizationAsync(string userId, OrganizationSetupDto dto)
    {
        var user = await _context.Users
            .Include(u => u.Organization)
            .FirstOrDefaultAsync(u => u.Id == userId);

        if (user == null)
        {
            return false;
        }

        if (user.Organization == null)
        {
            var org = new Organization
            {
                Id = Guid.NewGuid().ToString(),
                Name = dto.Name,
                Description = dto.Description,
                Website = dto.Website,
                CreatedAt = DateTime.UtcNow
            };

            _context.Organizations.Add(org);
            user.OrganizationId = org.Id;
        }
        else
        {
            user.Organization.Name = dto.Name;
            user.Organization.Description = dto.Description;
            user.Organization.Website = dto.Website;
            user.Organization.UpdatedAt = DateTime.UtcNow;
        }

        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<bool> SetupFirstBotAsync(string userId, BotSetupDto dto)
    {
        var user = await _context.Users.FindAsync(userId);
        if (user == null)
        {
            return false;
        }

        var bot = new Bot
        {
            Id = Guid.NewGuid().ToString(),
            Name = dto.Name,
            Description = dto.Description,
            SystemPrompt = dto.Purpose,
            UserId = userId,
            OrganizationId = user.OrganizationId,
            CreatedAt = DateTime.UtcNow,
            IsActive = true
        };

        _context.Bots.Add(bot);
        await _context.SaveChangesAsync();

        return true;
    }
}
