using OrkinosaiCMS.Core.Interfaces.Services;

namespace SiteChatCMS.Infrastructure.Services;

/// <summary>
/// Simple in-memory user service for demo purposes
/// TODO: Replace with proper user service implementation
/// </summary>
public class UserService : IUserService
{
    private readonly Dictionary<string, User> _usersByEmail = new();
    private readonly Dictionary<int, User> _usersById = new();

    public UserService()
    {
        // Add a demo user for testing
        var demoUser = new User
        {
            Id = 1,
            Email = "demo@example.com",
            DisplayName = "Demo User"
        };
        
        _usersByEmail[demoUser.Email] = demoUser;
        _usersById[demoUser.Id] = demoUser;
    }

    public Task<User?> GetByEmailAsync(string email)
    {
        _usersByEmail.TryGetValue(email, out var user);
        return Task.FromResult(user);
    }

    public Task<User?> GetByIdAsync(int id)
    {
        _usersById.TryGetValue(id, out var user);
        return Task.FromResult(user);
    }
}
