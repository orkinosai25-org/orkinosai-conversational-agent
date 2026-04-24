namespace SiteChatCMS.Core.Common;

/// <summary>
/// Base entity class with common properties
/// </summary>
public abstract class BaseEntity
{
    /// <summary>
    /// Unique identifier
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Date when entity was created
    /// </summary>
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    /// <summary>
    /// Date when entity was last updated
    /// </summary>
    public DateTime? UpdatedAt { get; set; }
}
