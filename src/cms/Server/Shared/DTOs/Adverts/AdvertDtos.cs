namespace SiteChatCMS.Shared.DTOs.Adverts;

/// <summary>
/// Advert tier information returned to clients
/// </summary>
public class AdvertTierDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public decimal MonthlyPrice { get; set; }
    public int MaxDurationDays { get; set; }
    public List<string> AllowedPlacements { get; set; } = new();
    public bool IsPriorityPlacement { get; set; }
    public int MaxImpressions { get; set; }
    public bool IsActive { get; set; }
}

/// <summary>
/// Full advert details returned to clients
/// </summary>
public class AdvertDto
{
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string? ImageUrl { get; set; }
    public string TargetUrl { get; set; } = string.Empty;
    public int TierId { get; set; }
    public string TierName { get; set; } = string.Empty;
    public string Placement { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public string AdvertiserName { get; set; } = string.Empty;
    public string AdvertiserEmail { get; set; } = string.Empty;
    public DateTime StartDate { get; set; }
    public DateTime EndDate { get; set; }
    public int ImpressionCount { get; set; }
    public int ClickCount { get; set; }
    public decimal AmountPaid { get; set; }
    public string? Notes { get; set; }
    public DateTime CreatedAt { get; set; }
}

/// <summary>
/// Payload for creating / purchasing a new advert campaign
/// </summary>
public class CreateAdvertDto
{
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string? ImageUrl { get; set; }
    public string TargetUrl { get; set; } = string.Empty;
    public int TierId { get; set; }
    public string Placement { get; set; } = string.Empty;
    public string AdvertiserName { get; set; } = string.Empty;
    public string AdvertiserEmail { get; set; } = string.Empty;
    public DateTime StartDate { get; set; }
    public DateTime EndDate { get; set; }
}

/// <summary>
/// Payload for admin edits to an existing advert
/// </summary>
public class UpdateAdvertDto
{
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string? ImageUrl { get; set; }
    public string TargetUrl { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public DateTime StartDate { get; set; }
    public DateTime EndDate { get; set; }
    public string? Notes { get; set; }
}

/// <summary>
/// Aggregate statistics for the admin advert dashboard
/// </summary>
public class AdvertStatsDto
{
    public int TotalAdverts { get; set; }
    public int ActiveAdverts { get; set; }
    public int PendingAdverts { get; set; }
    public int ExpiredAdverts { get; set; }
    public long TotalImpressions { get; set; }
    public long TotalClicks { get; set; }
    public decimal TotalRevenue { get; set; }
}
