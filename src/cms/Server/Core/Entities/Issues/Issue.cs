using SiteChatCMS.Core.Common;

namespace SiteChatCMS.Core.Entities.Issues;

/// <summary>
/// Represents a support issue submitted by a user
/// </summary>
public class Issue : BaseEntity
{
    /// <summary>Short headline describing the issue</summary>
    public string Title { get; set; } = string.Empty;

    /// <summary>Full description of the issue</summary>
    public string Description { get; set; } = string.Empty;

    /// <summary>Category of the issue</summary>
    public IssueType Type { get; set; } = IssueType.Other;

    /// <summary>Urgency of the issue</summary>
    public IssuePriority Priority { get; set; } = IssuePriority.Medium;

    /// <summary>Current lifecycle status</summary>
    public IssueStatus Status { get; set; } = IssueStatus.Open;

    /// <summary>Name of the person who submitted the issue</summary>
    public string SubmitterName { get; set; } = string.Empty;

    /// <summary>Contact email of the submitter</summary>
    public string SubmitterEmail { get; set; } = string.Empty;

    /// <summary>Internal admin notes / resolution details</summary>
    public string? AdminNotes { get; set; }

    /// <summary>When the issue was last updated by an admin</summary>
    public DateTime? ResolvedAt { get; set; }
}
