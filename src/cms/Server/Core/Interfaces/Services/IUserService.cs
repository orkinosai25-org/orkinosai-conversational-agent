namespace OrkinosaiCMS.Core.Interfaces.Services;

/// <summary>
/// Service interface for user management
/// </summary>
public interface IUserService
{
    /// <summary>
    /// Get user by email
    /// </summary>
    Task<User?> GetByEmailAsync(string email);
    
    /// <summary>
    /// Get user by ID
    /// </summary>
    Task<User?> GetByIdAsync(int id);
}

/// <summary>
/// Simple user entity for demo purposes
/// TODO: Replace with proper user entity
/// </summary>
public class User
{
    public int Id { get; set; }
    public string Email { get; set; } = string.Empty;
    public string DisplayName { get; set; } = string.Empty;
}
