using PapaganCMS.Core.Common;

namespace PapaganCMS.Core.Entities.Identity;

/// <summary>
/// Organization entity for multi-tenant support
/// </summary>
public class Organization : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? Website { get; set; }
    public string? LogoUrl { get; set; }
    public int MaxUsers { get; set; } = 5;
    public int MaxBots { get; set; } = 1;
    public bool IsActive { get; set; } = true;
    public string? SubscriptionId { get; set; }
    
    // Navigation
    public virtual ICollection<ApplicationUser> Users { get; set; } = new List<ApplicationUser>();
    public virtual ICollection<Bot> Bots { get; set; } = new List<Bot>();
}
