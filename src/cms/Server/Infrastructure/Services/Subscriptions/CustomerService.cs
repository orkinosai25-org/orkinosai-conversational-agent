using OrkinosaiCMS.Core.Entities.Subscriptions;
using OrkinosaiCMS.Core.Interfaces.Services;

namespace OrkinosaiCMS.Infrastructure.Services.Subscriptions;

/// <summary>
/// Simple in-memory implementation of customer service
/// TODO: Replace with database-backed implementation
/// </summary>
public class CustomerService : ICustomerService
{
    private readonly Dictionary<int, Customer> _customers = new();
    private readonly Dictionary<int, Customer> _customersByUserId = new();
    private readonly Dictionary<string, Customer> _customersByStripeId = new();
    private int _nextId = 1;

    public Task<Customer?> GetByIdAsync(int id)
    {
        _customers.TryGetValue(id, out var customer);
        return Task.FromResult(customer);
    }

    public Task<Customer?> GetByUserIdAsync(int userId)
    {
        _customersByUserId.TryGetValue(userId, out var customer);
        return Task.FromResult(customer);
    }

    public Task<Customer?> GetByStripeCustomerIdAsync(string stripeCustomerId)
    {
        _customersByStripeId.TryGetValue(stripeCustomerId, out var customer);
        return Task.FromResult(customer);
    }

    public Task<Customer> CreateAsync(Customer customer)
    {
        customer.Id = _nextId++;
        customer.CreatedAt = DateTime.UtcNow;
        
        _customers[customer.Id] = customer;
        _customersByUserId[customer.UserId] = customer;
        _customersByStripeId[customer.StripeCustomerId] = customer;
        
        return Task.FromResult(customer);
    }

    public Task<Customer> UpdateAsync(Customer customer)
    {
        customer.UpdatedAt = DateTime.UtcNow;
        
        _customers[customer.Id] = customer;
        _customersByUserId[customer.UserId] = customer;
        _customersByStripeId[customer.StripeCustomerId] = customer;
        
        return Task.FromResult(customer);
    }

    public Task<bool> DeleteAsync(int id)
    {
        if (_customers.TryGetValue(id, out var customer))
        {
            _customers.Remove(id);
            _customersByUserId.Remove(customer.UserId);
            _customersByStripeId.Remove(customer.StripeCustomerId);
            return Task.FromResult(true);
        }
        
        return Task.FromResult(false);
    }
}
