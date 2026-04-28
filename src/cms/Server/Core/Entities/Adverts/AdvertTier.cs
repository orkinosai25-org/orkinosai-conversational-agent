namespace SiteChatCMS.Core.Entities.Adverts;

/// <summary>
/// Represents a purchasable advertising tier with its features and pricing
/// </summary>
public class AdvertTier
{
    /// <summary>Unique identifier</summary>
    public int Id { get; set; }

    /// <summary>Display name (e.g. "Basic", "Standard", "Premium")</summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>Short description shown to customers</summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>Monthly price in USD</summary>
    public decimal MonthlyPrice { get; set; }

    /// <summary>Maximum campaign duration in days</summary>
    public int MaxDurationDays { get; set; }

    /// <summary>Placements available to this tier</summary>
    public List<AdvertPlacement> AllowedPlacements { get; set; } = new();

    /// <summary>Whether this tier gets priority ordering in its placements</summary>
    public bool IsPriorityPlacement { get; set; }

    /// <summary>Maximum impressions per campaign (0 = unlimited)</summary>
    public int MaxImpressions { get; set; }

    /// <summary>Whether this tier is available for purchase</summary>
    public bool IsActive { get; set; } = true;
}
