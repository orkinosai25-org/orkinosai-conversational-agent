namespace SiteChatCMS.Core.Entities.Adverts;

/// <summary>
/// Lifecycle status of an advert
/// </summary>
public enum AdvertStatus
{
    /// <summary>Submitted and awaiting admin review</summary>
    Pending = 0,

    /// <summary>Approved and currently serving</summary>
    Active = 1,

    /// <summary>Temporarily paused by admin or advertiser</summary>
    Paused = 2,

    /// <summary>Past its end date</summary>
    Expired = 3,

    /// <summary>Rejected by admin</summary>
    Rejected = 4
}
