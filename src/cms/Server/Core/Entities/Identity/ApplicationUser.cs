using Microsoft.AspNetCore.Identity;

namespace SiteChatCMS.Core.Entities.Identity;

/// <summary>
/// Application user entity extending ASP.NET Identity
/// </summary>
public class ApplicationUser : IdentityUser
{
    public string? FirstName { get; set; }
    public string? LastName { get; set; }
    public string? DisplayName { get; set; }
    public string? AvatarUrl { get; set; }
    public string? OrganizationId { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? LastLoginAt { get; set; }
    public bool IsActive { get; set; } = true;
    
    // Onboarding
    public bool HasCompletedOnboarding { get; set; } = false;
    public string? OnboardingStep { get; set; }
    
    // Navigation
    public virtual Organization? Organization { get; set; }
    public virtual ICollection<Bot> Bots { get; set; } = new List<Bot>();
}
