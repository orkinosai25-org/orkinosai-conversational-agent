using PapaganCMS.Core.Entities.Subscriptions;
using PapaganCMS.Core.Interfaces.Services;

namespace PapaganCMS.Infrastructure.Services.Subscriptions;

/// <summary>
/// Simple in-memory implementation of subscription service
/// TODO: Replace with database-backed implementation
/// </summary>
public class SubscriptionService : ISubscriptionService
{
    private readonly Dictionary<int, Subscription> _subscriptions = new();
    private readonly Dictionary<int, List<Subscription>> _subscriptionsByCustomerId = new();
    private int _nextId = 1;
    private readonly ICustomerService _customerService;

    public SubscriptionService(ICustomerService customerService)
    {
        _customerService = customerService;
    }

    public Task<Subscription?> GetByIdAsync(int id)
    {
        _subscriptions.TryGetValue(id, out var subscription);
        return Task.FromResult(subscription);
    }

    public Task<Subscription?> GetActiveSubscriptionByCustomerIdAsync(int customerId)
    {
        if (_subscriptionsByCustomerId.TryGetValue(customerId, out var subscriptions))
        {
            var activeSubscription = subscriptions
                .Where(s => s.Status == SubscriptionStatus.Active || s.Status == SubscriptionStatus.Trialing)
                .OrderByDescending(s => s.CreatedAt)
                .FirstOrDefault();
            
            return Task.FromResult(activeSubscription);
        }
        
        return Task.FromResult<Subscription?>(null);
    }

    public async Task<Subscription?> GetActiveSubscriptionByUserIdAsync(int userId)
    {
        var customer = await _customerService.GetByUserIdAsync(userId);
        if (customer == null)
            return null;

        return await GetActiveSubscriptionByCustomerIdAsync(customer.Id);
    }

    public Task<Subscription> CreateAsync(Subscription subscription)
    {
        subscription.Id = _nextId++;
        subscription.CreatedAt = DateTime.UtcNow;
        
        _subscriptions[subscription.Id] = subscription;
        
        if (!_subscriptionsByCustomerId.ContainsKey(subscription.CustomerId))
        {
            _subscriptionsByCustomerId[subscription.CustomerId] = new List<Subscription>();
        }
        _subscriptionsByCustomerId[subscription.CustomerId].Add(subscription);
        
        return Task.FromResult(subscription);
    }

    public Task<Subscription> UpdateAsync(Subscription subscription)
    {
        subscription.UpdatedAt = DateTime.UtcNow;
        _subscriptions[subscription.Id] = subscription;
        
        return Task.FromResult(subscription);
    }

    public async Task<bool> CancelAsync(int subscriptionId, bool cancelAtPeriodEnd = true)
    {
        var subscription = await GetByIdAsync(subscriptionId);
        if (subscription == null)
            return false;

        subscription.CancelAtPeriodEnd = cancelAtPeriodEnd;
        subscription.Status = cancelAtPeriodEnd ? subscription.Status : SubscriptionStatus.Canceled;
        subscription.CanceledAt = DateTime.UtcNow;
        subscription.UpdatedAt = DateTime.UtcNow;

        await UpdateAsync(subscription);
        return true;
    }

    public Task<bool> HasReachedWebsiteLimitAsync(int userId)
    {
        // TODO: Implement when website tracking is added
        return Task.FromResult(false);
    }

    public Task<bool> HasReachedStorageLimitAsync(int userId, long currentStorageBytes)
    {
        // TODO: Implement when storage tracking is added
        return Task.FromResult(false);
    }

    public TierLimits GetTierLimits(SubscriptionTier tier)
    {
        return tier switch
        {
            SubscriptionTier.Free => new TierLimits
            {
                MaxWebsites = 1,
                MaxStorageBytes = 500L * 1024 * 1024, // 500 MB
                MaxBandwidthBytes = 10L * 1024 * 1024 * 1024, // 10 GB
                MaxCustomDomains = 0,
                HasAds = true,
                HasBranding = true
            },
            SubscriptionTier.Starter => new TierLimits
            {
                MaxWebsites = 3,
                MaxStorageBytes = 5L * 1024 * 1024 * 1024, // 5 GB
                MaxBandwidthBytes = 25L * 1024 * 1024 * 1024, // 25 GB
                MaxCustomDomains = 1,
                HasAds = false,
                HasBranding = false
            },
            SubscriptionTier.Pro => new TierLimits
            {
                MaxWebsites = 10,
                MaxStorageBytes = 25L * 1024 * 1024 * 1024, // 25 GB
                MaxBandwidthBytes = 100L * 1024 * 1024 * 1024, // 100 GB
                MaxCustomDomains = 10,
                HasAds = false,
                HasBranding = false
            },
            SubscriptionTier.Business => new TierLimits
            {
                MaxWebsites = 50,
                MaxStorageBytes = 100L * 1024 * 1024 * 1024, // 100 GB
                MaxBandwidthBytes = 500L * 1024 * 1024 * 1024, // 500 GB
                MaxCustomDomains = 50,
                HasAds = false,
                HasBranding = false
            },
            _ => throw new ArgumentException($"Unknown tier: {tier}")
        };
    }
}
