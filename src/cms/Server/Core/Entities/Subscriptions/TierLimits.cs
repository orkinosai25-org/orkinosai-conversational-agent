namespace PapaganCMS.Core.Entities.Subscriptions;

/// <summary>
/// Represents the limits and features for a subscription tier
/// </summary>
public class TierLimits
{
    /// <summary>
    /// Maximum number of websites allowed
    /// </summary>
    public int MaxWebsites { get; set; }

    /// <summary>
    /// Maximum storage in bytes
    /// </summary>
    public long MaxStorageBytes { get; set; }

    /// <summary>
    /// Maximum bandwidth in bytes
    /// </summary>
    public long MaxBandwidthBytes { get; set; }

    /// <summary>
    /// Maximum number of custom domains
    /// </summary>
    public int MaxCustomDomains { get; set; }

    /// <summary>
    /// Whether tier shows advertisements
    /// </summary>
    public bool HasAds { get; set; }

    /// <summary>
    /// Whether tier requires platform branding
    /// </summary>
    public bool HasBranding { get; set; }
}
