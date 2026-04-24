using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using SiteChatCMS.Core.Entities.Identity;
using SiteChatCMS.Core.Interfaces.Services;
using SiteChatCMS.Infrastructure.Data;
using SiteChatCMS.Shared.DTOs.Auth;

namespace SiteChatCMS.Infrastructure.Services.Auth;

public class AuthService : IAuthService
{
    private readonly UserManager<ApplicationUser> _userManager;
    private readonly SignInManager<ApplicationUser> _signInManager;
    private readonly ApplicationDbContext _context;
    private readonly IHttpContextAccessor _httpContextAccessor;

    public AuthService(
        UserManager<ApplicationUser> userManager,
        SignInManager<ApplicationUser> signInManager,
        ApplicationDbContext context,
        IHttpContextAccessor httpContextAccessor)
    {
        _userManager = userManager;
        _signInManager = signInManager;
        _context = context;
        _httpContextAccessor = httpContextAccessor;
    }

    public async Task<AuthResponseDto> RegisterAsync(RegisterDto dto)
    {
        // Validate passwords match
        if (dto.Password != dto.ConfirmPassword)
        {
            return new AuthResponseDto
            {
                Success = false,
                Message = "Passwords do not match"
            };
        }

        // Check if user already exists
        var existingUser = await _userManager.FindByEmailAsync(dto.Email);
        if (existingUser != null)
        {
            return new AuthResponseDto
            {
                Success = false,
                Message = "Email already registered"
            };
        }

        // Create new user
        var user = new ApplicationUser
        {
            UserName = dto.Email,
            Email = dto.Email,
            FirstName = dto.FirstName,
            LastName = dto.LastName,
            DisplayName = $"{dto.FirstName} {dto.LastName}".Trim(),
            CreatedAt = DateTime.UtcNow,
            HasCompletedOnboarding = false,
            OnboardingStep = "welcome"
        };

        var result = await _userManager.CreateAsync(user, dto.Password);
        if (!result.Succeeded)
        {
            return new AuthResponseDto
            {
                Success = false,
                Message = string.Join(", ", result.Errors.Select(e => e.Description))
            };
        }

        // Create organization if provided
        if (!string.IsNullOrWhiteSpace(dto.OrganizationName))
        {
            var org = new Organization
            {
                Id = Guid.NewGuid().ToString(),
                Name = dto.OrganizationName,
                CreatedAt = DateTime.UtcNow
            };
            _context.Organizations.Add(org);
            await _context.SaveChangesAsync();

            user.OrganizationId = org.Id;
            await _userManager.UpdateAsync(user);
        }

        // Sign in the user
        await _signInManager.SignInAsync(user, isPersistent: false);

        return new AuthResponseDto
        {
            Success = true,
            Message = "Registration successful",
            User = MapToUserDto(user)
        };
    }

    public async Task<AuthResponseDto> LoginAsync(LoginDto dto)
    {
        var user = await _userManager.FindByEmailAsync(dto.Email);
        if (user == null)
        {
            return new AuthResponseDto
            {
                Success = false,
                Message = "Invalid email or password"
            };
        }

        var result = await _signInManager.PasswordSignInAsync(user, dto.Password, dto.RememberMe, lockoutOnFailure: false);
        if (!result.Succeeded)
        {
            return new AuthResponseDto
            {
                Success = false,
                Message = "Invalid email or password"
            };
        }

        // Update last login
        user.LastLoginAt = DateTime.UtcNow;
        await _userManager.UpdateAsync(user);

        return new AuthResponseDto
        {
            Success = true,
            Message = "Login successful",
            User = MapToUserDto(user)
        };
    }

    public async Task<bool> LogoutAsync(string userId)
    {
        await _signInManager.SignOutAsync();
        return true;
    }

    public async Task<AuthResponseDto> ForgotPasswordAsync(ForgotPasswordDto dto)
    {
        var user = await _userManager.FindByEmailAsync(dto.Email);
        if (user == null)
        {
            // Don't reveal that the user does not exist
            return new AuthResponseDto
            {
                Success = true,
                Message = "If an account exists, a password reset link has been sent"
            };
        }

        var token = await _userManager.GeneratePasswordResetTokenAsync(user);
        // TODO: Send email with token
        // For now, just return success
        return new AuthResponseDto
        {
            Success = true,
            Message = "If an account exists, a password reset link has been sent"
        };
    }

    public async Task<AuthResponseDto> ResetPasswordAsync(ResetPasswordDto dto)
    {
        if (dto.Password != dto.ConfirmPassword)
        {
            return new AuthResponseDto
            {
                Success = false,
                Message = "Passwords do not match"
            };
        }

        var user = await _userManager.FindByEmailAsync(dto.Email);
        if (user == null)
        {
            return new AuthResponseDto
            {
                Success = false,
                Message = "Invalid reset token"
            };
        }

        var result = await _userManager.ResetPasswordAsync(user, dto.Token, dto.Password);
        if (!result.Succeeded)
        {
            return new AuthResponseDto
            {
                Success = false,
                Message = string.Join(", ", result.Errors.Select(e => e.Description))
            };
        }

        return new AuthResponseDto
        {
            Success = true,
            Message = "Password reset successful"
        };
    }

    public async Task<UserDto?> GetUserAsync(string userId)
    {
        var user = await _context.Users
            .Include(u => u.Organization)
            .FirstOrDefaultAsync(u => u.Id == userId);

        return user == null ? null : MapToUserDto(user);
    }

    public async Task<ApplicationUser?> GetCurrentUserAsync()
    {
        var httpContext = _httpContextAccessor.HttpContext;
        if (httpContext?.User?.Identity?.IsAuthenticated != true)
        {
            return null;
        }

        var userId = _userManager.GetUserId(httpContext.User);
        if (string.IsNullOrEmpty(userId))
        {
            return null;
        }

        return await _context.Users
            .Include(u => u.Organization)
            .FirstOrDefaultAsync(u => u.Id == userId);
    }

    private UserDto MapToUserDto(ApplicationUser user)
    {
        return new UserDto
        {
            Id = user.Id,
            Email = user.Email ?? string.Empty,
            DisplayName = user.DisplayName,
            FirstName = user.FirstName,
            LastName = user.LastName,
            AvatarUrl = user.AvatarUrl,
            OrganizationId = user.OrganizationId,
            OrganizationName = user.Organization?.Name,
            HasCompletedOnboarding = user.HasCompletedOnboarding,
            OnboardingStep = user.OnboardingStep
        };
    }
}
