namespace SiteChatCMS.Core.Entities.Adverts;

/// <summary>
/// Where an advert is displayed
/// </summary>
public enum AdvertPlacement
{
    /// <summary>Footer of the chat widget — included in the cheapest (Basic) tier</summary>
    ChatFooter = 0,

    /// <summary>Sidebar adjacent to the chat widget</summary>
    ChatSidebar = 1,

    /// <summary>Banner above the chat widget</summary>
    ChatBanner = 2,

    /// <summary>Homepage of the hosted site</summary>
    HomePage = 3
}
