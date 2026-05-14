namespace SiteChatCMS.Core.Entities.Issues;

/// <summary>
/// Lifecycle status of a support issue
/// </summary>
public enum IssueStatus
{
    /// <summary>Newly submitted, awaiting triage</summary>
    Open,

    /// <summary>Issue has been picked up and is being worked on</summary>
    InProgress,

    /// <summary>A fix or answer has been provided</summary>
    Resolved,

    /// <summary>Issue is closed (no further action required)</summary>
    Closed
}
