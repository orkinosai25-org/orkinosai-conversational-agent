using PapaganCMS.Core.Entities.Identity;
using PapaganCMS.Shared.DTOs.Auth;

namespace PapaganCMS.Core.Interfaces.Services;

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
