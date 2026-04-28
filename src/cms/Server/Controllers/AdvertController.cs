using Microsoft.AspNetCore.Mvc;
using SiteChatCMS.Core.Entities.Adverts;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Shared.DTOs.Adverts;

namespace SiteChatCMS.Controllers;

/// <summary>
/// API controller for advert management.
/// Admin endpoints are prefixed with /api/advert/admin.
/// Customer-facing endpoints are prefixed with /api/advert.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class AdvertController : ControllerBase
{
    private readonly IAdvertService _advertService;
    private readonly ILogger<AdvertController> _logger;

    public AdvertController(IAdvertService advertService, ILogger<AdvertController> logger)
    {
        _advertService = advertService;
        _logger = logger;
    }

    // ── Tier endpoints ───────────────────────────────────────────────────────

    /// <summary>Get all advert tiers (used by customer buy page)</summary>
    [HttpGet("tiers")]
    [ProducesResponseType(typeof(IEnumerable<AdvertTierDto>), 200)]
    public IActionResult GetTiers()
    {
        var tiers = _advertService.GetAllTiers().Select(MapTier);
        return Ok(tiers);
    }

    /// <summary>Get a specific tier by ID</summary>
    [HttpGet("tiers/{id:int}")]
    [ProducesResponseType(typeof(AdvertTierDto), 200)]
    [ProducesResponseType(404)]
    public IActionResult GetTier(int id)
    {
        var tier = _advertService.GetTierById(id);
        if (tier == null) return NotFound();
        return Ok(MapTier(tier));
    }

    // ── Public / customer endpoints ──────────────────────────────────────────

    /// <summary>
    /// Purchase / submit a new advert campaign.
    /// In production this would be gated behind authentication and a payment step.
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof(AdvertDto), 201)]
    [ProducesResponseType(400)]
    public async Task<IActionResult> CreateAdvert([FromBody] CreateAdvertDto dto)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(dto.Title))
                return BadRequest("Title is required.");
            if (string.IsNullOrWhiteSpace(dto.TargetUrl))
                return BadRequest("Target URL is required.");
            if (dto.TierId <= 0)
                return BadRequest("A valid tier must be selected.");

            var tier = _advertService.GetTierById(dto.TierId);
            if (tier == null)
                return BadRequest("Selected tier does not exist.");

            if (!Enum.TryParse<AdvertPlacement>(dto.Placement, out var placement))
                return BadRequest("Invalid placement value.");

            if (!tier.AllowedPlacements.Contains(placement))
                return BadRequest($"Placement '{dto.Placement}' is not available for the '{tier.Name}' tier.");

            if (dto.EndDate <= dto.StartDate)
                return BadRequest("End date must be after start date.");

            var maxDuration = (dto.EndDate - dto.StartDate).Days;
            if (maxDuration > tier.MaxDurationDays)
                return BadRequest($"Campaign duration exceeds the maximum of {tier.MaxDurationDays} days for this tier.");

            var advert = new Advert
            {
                Title = dto.Title,
                Description = dto.Description,
                ImageUrl = dto.ImageUrl,
                TargetUrl = dto.TargetUrl,
                TierId = dto.TierId,
                Placement = placement,
                AdvertiserName = dto.AdvertiserName,
                AdvertiserEmail = dto.AdvertiserEmail,
                StartDate = dto.StartDate.ToUniversalTime(),
                EndDate = dto.EndDate.ToUniversalTime(),
                AmountPaid = tier.MonthlyPrice
            };

            var created = await _advertService.CreateAdvertAsync(advert);
            return CreatedAtAction(nameof(GetAdvert), new { id = created.Id }, MapAdvert(created));
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating advert");
            return StatusCode(500, "An error occurred while creating the advert.");
        }
    }

    /// <summary>Get active adverts for a specific placement (used by widget renderer)</summary>
    [HttpGet("placement/{placement}")]
    [ProducesResponseType(typeof(IEnumerable<AdvertDto>), 200)]
    public async Task<IActionResult> GetAdvertsByPlacement(string placement)
    {
        if (!Enum.TryParse<AdvertPlacement>(placement, true, out var placementEnum))
            return BadRequest("Invalid placement value.");

        var adverts = await _advertService.GetAdvertsByPlacementAsync(placementEnum);
        return Ok(adverts.Select(MapAdvert));
    }

    /// <summary>Get a single advert by ID</summary>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(AdvertDto), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetAdvert(int id)
    {
        var advert = await _advertService.GetAdvertByIdAsync(id);
        if (advert == null) return NotFound();
        return Ok(MapAdvert(advert));
    }

    /// <summary>Record an impression for an advert</summary>
    [HttpPost("{id:int}/impression")]
    [ProducesResponseType(204)]
    public async Task<IActionResult> RecordImpression(int id)
    {
        await _advertService.RecordImpressionAsync(id);
        return NoContent();
    }

    /// <summary>Record a click for an advert</summary>
    [HttpPost("{id:int}/click")]
    [ProducesResponseType(204)]
    public async Task<IActionResult> RecordClick(int id)
    {
        await _advertService.RecordClickAsync(id);
        return NoContent();
    }

    // ── Admin endpoints ──────────────────────────────────────────────────────

    /// <summary>Admin: get all adverts</summary>
    [HttpGet("admin/all")]
    [ProducesResponseType(typeof(IEnumerable<AdvertDto>), 200)]
    public async Task<IActionResult> GetAllAdverts()
    {
        var adverts = await _advertService.GetAllAdvertsAsync();
        return Ok(adverts.Select(MapAdvert));
    }

    /// <summary>Admin: get dashboard statistics</summary>
    [HttpGet("admin/stats")]
    [ProducesResponseType(typeof(AdvertStatsDto), 200)]
    public async Task<IActionResult> GetStats()
    {
        var adverts = (await _advertService.GetAllAdvertsAsync()).ToList();
        var stats = new AdvertStatsDto
        {
            TotalAdverts = adverts.Count,
            ActiveAdverts = adverts.Count(a => a.Status == AdvertStatus.Active),
            PendingAdverts = adverts.Count(a => a.Status == AdvertStatus.Pending),
            ExpiredAdverts = adverts.Count(a => a.Status == AdvertStatus.Expired),
            TotalImpressions = adverts.Sum(a => (long)a.ImpressionCount),
            TotalClicks = adverts.Sum(a => (long)a.ClickCount),
            TotalRevenue = adverts.Sum(a => a.AmountPaid)
        };
        return Ok(stats);
    }

    /// <summary>Admin: update an advert</summary>
    [HttpPut("admin/{id:int}")]
    [ProducesResponseType(typeof(AdvertDto), 200)]
    [ProducesResponseType(400)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> UpdateAdvert(int id, [FromBody] UpdateAdvertDto dto)
    {
        try
        {
            var existing = await _advertService.GetAdvertByIdAsync(id);
            if (existing == null) return NotFound();

            existing.Title = dto.Title;
            existing.Description = dto.Description;
            existing.ImageUrl = dto.ImageUrl;
            existing.TargetUrl = dto.TargetUrl;
            existing.Notes = dto.Notes;
            existing.StartDate = dto.StartDate.ToUniversalTime();
            existing.EndDate = dto.EndDate.ToUniversalTime();

            if (!string.IsNullOrEmpty(dto.Status) && Enum.TryParse<AdvertStatus>(dto.Status, out var status))
                existing.Status = status;

            var updated = await _advertService.UpdateAdvertAsync(existing);
            return Ok(MapAdvert(updated));
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error updating advert {Id}", id);
            return StatusCode(500, "An error occurred while updating the advert.");
        }
    }

    /// <summary>Admin: delete an advert</summary>
    [HttpDelete("admin/{id:int}")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> DeleteAdvert(int id)
    {
        var deleted = await _advertService.DeleteAdvertAsync(id);
        if (!deleted) return NotFound();
        return NoContent();
    }

    /// <summary>Admin: approve a pending advert</summary>
    [HttpPost("admin/{id:int}/approve")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> ApproveAdvert(int id)
    {
        var success = await _advertService.ApproveAdvertAsync(id);
        if (!success) return NotFound();
        return NoContent();
    }

    /// <summary>Admin: pause an active advert</summary>
    [HttpPost("admin/{id:int}/pause")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> PauseAdvert(int id)
    {
        var success = await _advertService.PauseAdvertAsync(id);
        if (!success) return NotFound();
        return NoContent();
    }

    /// <summary>Admin: reject a pending advert</summary>
    [HttpPost("admin/{id:int}/reject")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> RejectAdvert(int id)
    {
        var success = await _advertService.RejectAdvertAsync(id);
        if (!success) return NotFound();
        return NoContent();
    }

    // ── Mappers ──────────────────────────────────────────────────────────────

    private static AdvertTierDto MapTier(AdvertTier tier) => new()
    {
        Id = tier.Id,
        Name = tier.Name,
        Description = tier.Description,
        MonthlyPrice = tier.MonthlyPrice,
        MaxDurationDays = tier.MaxDurationDays,
        AllowedPlacements = tier.AllowedPlacements.Select(p => p.ToString()).ToList(),
        IsPriorityPlacement = tier.IsPriorityPlacement,
        MaxImpressions = tier.MaxImpressions,
        IsActive = tier.IsActive
    };

    private static AdvertDto MapAdvert(Advert advert) => new()
    {
        Id = advert.Id,
        Title = advert.Title,
        Description = advert.Description,
        ImageUrl = advert.ImageUrl,
        TargetUrl = advert.TargetUrl,
        TierId = advert.TierId,
        TierName = advert.Tier?.Name ?? string.Empty,
        Placement = advert.Placement.ToString(),
        Status = advert.Status.ToString(),
        AdvertiserName = advert.AdvertiserName,
        AdvertiserEmail = advert.AdvertiserEmail,
        StartDate = advert.StartDate,
        EndDate = advert.EndDate,
        ImpressionCount = advert.ImpressionCount,
        ClickCount = advert.ClickCount,
        AmountPaid = advert.AmountPaid,
        Notes = advert.Notes,
        CreatedAt = advert.CreatedAt
    };
}
