using SiteChatCMS.Core.Entities.Identity;
using SiteChatCMS.Shared.DTOs.Auth;

namespace SiteChatCMS.Core.Interfaces.Services;

public interface IAuthService
{
    Task<AuthResponseDto> RegisterAsync(RegisterDto dto);
    Task<AuthResponseDto> LoginAsync(LoginDto dto);
    Task<bool> LogoutAsync(string userId);
    Task<AuthResponseDto> ForgotPasswordAsync(ForgotPasswordDto dto);
    Task<AuthResponseDto> ResetPasswordAsync(ResetPasswordDto dto);
    Task<UserDto?> GetUserAsync(string userId);
    Task<ApplicationUser?> GetCurrentUserAsync();
}
