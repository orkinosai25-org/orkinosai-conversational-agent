using SiteChatCMS.Core.Entities.Adverts;
using SiteChatCMS.Core.Interfaces.Services;

namespace SiteChatCMS.Infrastructure.Services.Adverts;

/// <summary>
/// In-memory implementation of IAdvertService.
/// TODO: Replace with database-backed implementation for production.
/// </summary>
public class AdvertService : IAdvertService
{
    // ── Static tier definitions ──────────────────────────────────────────────

    private static readonly List<AdvertTier> _tiers = new()
    {
        new AdvertTier
        {
            Id = 1,
            Name = "Basic",
            Description = "Entry-level placement in the chat widget footer. Great for brand awareness on a budget.",
            MonthlyPrice = 9.99m,
            MaxDurationDays = 30,
            AllowedPlacements = new List<AdvertPlacement> { AdvertPlacement.ChatFooter },
            IsPriorityPlacement = false,
            MaxImpressions = 10_000,
            IsActive = true
        },
        new AdvertTier
        {
            Id = 2,
            Name = "Standard",
            Description = "Sidebar and chat banner placements for increased visibility.",
            MonthlyPrice = 24.99m,
            MaxDurationDays = 60,
            AllowedPlacements = new List<AdvertPlacement>
            {
                AdvertPlacement.ChatFooter,
                AdvertPlacement.ChatSidebar,
                AdvertPlacement.ChatBanner
            },
            IsPriorityPlacement = false,
            MaxImpressions = 50_000,
            IsActive = true
        },
        new AdvertTier
        {
            Id = 3,
            Name = "Premium",
            Description = "All placements including homepage, with priority ordering and unlimited impressions.",
            MonthlyPrice = 49.99m,
            MaxDurationDays = 90,
            AllowedPlacements = new List<AdvertPlacement>
            {
                AdvertPlacement.ChatFooter,
                AdvertPlacement.ChatSidebar,
                AdvertPlacement.ChatBanner,
                AdvertPlacement.HomePage
            },
            IsPriorityPlacement = true,
            MaxImpressions = 0, // unlimited
            IsActive = true
        }
    };

    // ── In-memory store ──────────────────────────────────────────────────────

    private readonly List<Advert> _adverts = new();
    private readonly object _syncLock = new();
    private int _nextId = 1;

    public AdvertService()
    {
        SeedSampleAdverts();
    }

    private void SeedSampleAdverts()
    {
        var now = DateTime.UtcNow;

        _adverts.AddRange(new[]
        {
            new Advert
            {
                Id = _nextId++,
                Title = "Boost Your Business with SiteChat",
                Description = "Reach thousands of visitors using our AI-powered chat widgets.",
                TargetUrl = "https://example.com/sitechat",
                TierId = 1,
                Tier = _tiers[0],
                Placement = AdvertPlacement.ChatFooter,
                Status = AdvertStatus.Active,
                AdvertiserName = "SiteChat Demo Co.",
                AdvertiserEmail = "ads@sitechat.demo",
                StartDate = now.AddDays(-5),
                EndDate = now.AddDays(25),
                ImpressionCount = 1_234,
                ClickCount = 47,
                AmountPaid = 9.99m,
                CreatedAt = now.AddDays(-6)
            },
            new Advert
            {
                Id = _nextId++,
                Title = "Premium Cloud Hosting — 50% Off First Month",
                Description = "Fast, reliable hosting for your next project. Use code CHAT50.",
                TargetUrl = "https://example.com/cloud",
                TierId = 2,
                Tier = _tiers[1],
                Placement = AdvertPlacement.ChatSidebar,
                Status = AdvertStatus.Active,
                AdvertiserName = "CloudHost Inc.",
                AdvertiserEmail = "marketing@cloudhost.demo",
                StartDate = now.AddDays(-10),
                EndDate = now.AddDays(50),
                ImpressionCount = 8_540,
                ClickCount = 312,
                AmountPaid = 24.99m,
                CreatedAt = now.AddDays(-11)
            },
            new Advert
            {
                Id = _nextId++,
                Title = "AI Writing Assistant — Try Free for 14 Days",
                Description = "Generate blog posts, ads and emails in seconds.",
                TargetUrl = "https://example.com/ai-writer",
                TierId = 3,
                Tier = _tiers[2],
                Placement = AdvertPlacement.HomePage,
                Status = AdvertStatus.Pending,
                AdvertiserName = "WriteAI Ltd.",
                AdvertiserEmail = "hello@writeai.demo",
                StartDate = now.AddDays(1),
                EndDate = now.AddDays(91),
                ImpressionCount = 0,
                ClickCount = 0,
                AmountPaid = 49.99m,
                CreatedAt = now
            }
        });
    }

    // ── IAdvertService implementation ────────────────────────────────────────

    public Task<IEnumerable<Advert>> GetAllAdvertsAsync() =>
        Task.FromResult<IEnumerable<Advert>>(_adverts.OrderByDescending(a => a.CreatedAt).ToList());

    public Task<IEnumerable<Advert>> GetActiveAdvertsAsync()
    {
        var now = DateTime.UtcNow;
        var active = _adverts
            .Where(a => a.Status == AdvertStatus.Active && a.StartDate <= now && a.EndDate >= now)
            .OrderByDescending(a => (a.Tier?.IsPriorityPlacement ?? false) ? 1 : 0)
            .ThenBy(a => a.CreatedAt)
            .ToList();
        return Task.FromResult<IEnumerable<Advert>>(active);
    }

    public Task<IEnumerable<Advert>> GetAdvertsByPlacementAsync(AdvertPlacement placement)
    {
        var now = DateTime.UtcNow;
        var filtered = _adverts
            .Where(a => a.Placement == placement
                     && a.Status == AdvertStatus.Active
                     && a.StartDate <= now
                     && a.EndDate >= now)
            .OrderByDescending(a => (a.Tier?.IsPriorityPlacement ?? false) ? 1 : 0)
            .ToList();
        return Task.FromResult<IEnumerable<Advert>>(filtered);
    }

    public Task<Advert?> GetAdvertByIdAsync(int id) =>
        Task.FromResult(_adverts.FirstOrDefault(a => a.Id == id));

    public Task<Advert> CreateAdvertAsync(Advert advert)
    {
        lock (_syncLock)
        {
            advert.Id = _nextId++;
            advert.CreatedAt = DateTime.UtcNow;
            advert.Status = AdvertStatus.Pending;
            advert.Tier = _tiers.FirstOrDefault(t => t.Id == advert.TierId);
            _adverts.Add(advert);
        }
        return Task.FromResult(advert);
    }

    public Task<Advert> UpdateAdvertAsync(Advert advert)
    {
        var index = _adverts.FindIndex(a => a.Id == advert.Id);
        if (index < 0)
            return Task.FromException<Advert>(new KeyNotFoundException($"Advert {advert.Id} not found."));

        advert.UpdatedAt = DateTime.UtcNow;
        advert.Tier = _tiers.FirstOrDefault(t => t.Id == advert.TierId);
        _adverts[index] = advert;
        return Task.FromResult(advert);
    }

    public Task<bool> DeleteAdvertAsync(int id)
    {
        var advert = _adverts.FirstOrDefault(a => a.Id == id);
        if (advert == null) return Task.FromResult(false);
        _adverts.Remove(advert);
        return Task.FromResult(true);
    }

    public async Task<bool> ApproveAdvertAsync(int id)
    {
        var advert = await GetAdvertByIdAsync(id);
        if (advert == null) return false;
        advert.Status = AdvertStatus.Active;
        advert.UpdatedAt = DateTime.UtcNow;
        return true;
    }

    public async Task<bool> PauseAdvertAsync(int id)
    {
        var advert = await GetAdvertByIdAsync(id);
        if (advert == null) return false;
        advert.Status = AdvertStatus.Paused;
        advert.UpdatedAt = DateTime.UtcNow;
        return true;
    }

    public async Task<bool> RejectAdvertAsync(int id)
    {
        var advert = await GetAdvertByIdAsync(id);
        if (advert == null) return false;
        advert.Status = AdvertStatus.Rejected;
        advert.UpdatedAt = DateTime.UtcNow;
        return true;
    }

    public async Task RecordImpressionAsync(int id)
    {
        var advert = await GetAdvertByIdAsync(id);
        if (advert != null)
        {
            lock (_syncLock)
            {
                // Re-check inside the lock in case the advert was removed concurrently
                if (_adverts.Contains(advert))
                    advert.ImpressionCount++;
            }
        }
    }

    public async Task RecordClickAsync(int id)
    {
        var advert = await GetAdvertByIdAsync(id);
        if (advert != null)
        {
            lock (_syncLock)
            {
                if (_adverts.Contains(advert))
                    advert.ClickCount++;
            }
        }
    }

    public IEnumerable<AdvertTier> GetAllTiers() => _tiers.AsReadOnly();

    public AdvertTier? GetTierById(int id) => _tiers.FirstOrDefault(t => t.Id == id);
}
