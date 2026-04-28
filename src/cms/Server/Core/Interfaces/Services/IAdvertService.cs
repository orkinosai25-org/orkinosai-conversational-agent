using SiteChatCMS.Core.Entities.Adverts;

namespace SiteChatCMS.Core.Interfaces.Services;

/// <summary>
/// Service for managing advertisement campaigns and tiers
/// </summary>
public interface IAdvertService
{
    // ── Advert CRUD ──────────────────────────────────────────────────────────

    /// <summary>Returns all adverts (admin view)</summary>
    Task<IEnumerable<Advert>> GetAllAdvertsAsync();

    /// <summary>Returns only adverts that are currently active and within their date range</summary>
    Task<IEnumerable<Advert>> GetActiveAdvertsAsync();

    /// <summary>Returns active adverts filtered by placement slot</summary>
    Task<IEnumerable<Advert>> GetAdvertsByPlacementAsync(AdvertPlacement placement);

    /// <summary>Returns a single advert by ID, or null if not found</summary>
    Task<Advert?> GetAdvertByIdAsync(int id);

    /// <summary>Creates a new advert (status defaults to Pending)</summary>
    Task<Advert> CreateAdvertAsync(Advert advert);

    /// <summary>Updates fields on an existing advert</summary>
    Task<Advert> UpdateAdvertAsync(Advert advert);

    /// <summary>Deletes an advert; returns false if not found</summary>
    Task<bool> DeleteAdvertAsync(int id);

    // ── Admin workflow ───────────────────────────────────────────────────────

    /// <summary>Sets an advert's status to Active</summary>
    Task<bool> ApproveAdvertAsync(int id);

    /// <summary>Sets an advert's status to Paused</summary>
    Task<bool> PauseAdvertAsync(int id);

    /// <summary>Sets an advert's status to Rejected</summary>
    Task<bool> RejectAdvertAsync(int id);

    // ── Metrics ─────────────────────────────────────────────────────────────

    /// <summary>Increments the impression counter for an advert</summary>
    Task RecordImpressionAsync(int id);

    /// <summary>Increments the click counter for an advert</summary>
    Task RecordClickAsync(int id);

    // ── Tier management ──────────────────────────────────────────────────────

    /// <summary>Returns all advert tiers</summary>
    IEnumerable<AdvertTier> GetAllTiers();

    /// <summary>Returns a single tier by ID, or null if not found</summary>
    AdvertTier? GetTierById(int id);
}
