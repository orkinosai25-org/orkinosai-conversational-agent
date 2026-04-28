using SiteChatCMS.Core.Common;

namespace SiteChatCMS.Core.Entities.Adverts;

/// <summary>
/// Represents a single advertisement campaign
/// </summary>
public class Advert : BaseEntity
{
    /// <summary>Headline / title of the advert</summary>
    public string Title { get; set; } = string.Empty;

    /// <summary>Body copy shown alongside the advert</summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>Optional URL of the advert image or banner</summary>
    public string? ImageUrl { get; set; }

    /// <summary>Destination URL when the advert is clicked</summary>
    public string TargetUrl { get; set; } = string.Empty;

    /// <summary>ID of the purchased advert tier</summary>
    public int TierId { get; set; }

    /// <summary>Navigation property to the tier</summary>
    public AdvertTier? Tier { get; set; }

    /// <summary>Where the advert is displayed</summary>
    public AdvertPlacement Placement { get; set; }

    /// <summary>Current lifecycle status</summary>
    public AdvertStatus Status { get; set; } = AdvertStatus.Pending;

    /// <summary>Name of the business or person running the advert</summary>
    public string AdvertiserName { get; set; } = string.Empty;

    /// <summary>Contact email of the advertiser</summary>
    public string AdvertiserEmail { get; set; } = string.Empty;

    /// <summary>When the campaign should start serving</summary>
    public DateTime StartDate { get; set; }

    /// <summary>When the campaign should stop serving</summary>
    public DateTime EndDate { get; set; }

    /// <summary>Running count of times this advert has been displayed</summary>
    public int ImpressionCount { get; set; }

    /// <summary>Running count of times this advert has been clicked</summary>
    public int ClickCount { get; set; }

    /// <summary>Amount paid (in USD) for this campaign</summary>
    public decimal AmountPaid { get; set; }

    /// <summary>Internal admin notes</summary>
    public string? Notes { get; set; }
}
