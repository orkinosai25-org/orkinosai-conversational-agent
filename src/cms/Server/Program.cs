using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using OrkinosaiCMS.Core.Interfaces.Services;
using PapaganCMS.Client.Pages;
using PapaganCMS.Components;
using PapaganCMS.Core.Entities.Identity;
using PapaganCMS.Core.Interfaces.Services;
using PapaganCMS.Infrastructure.Data;
using PapaganCMS.Infrastructure.Services;
using PapaganCMS.Infrastructure.Services.Auth;
using PapaganCMS.Infrastructure.Services.Bots;
using PapaganCMS.Infrastructure.Services.Onboarding;
using PapaganCMS.Infrastructure.Services.Subscriptions;

var builder = WebApplication.CreateBuilder(args);

// Add database context
builder.Services.AddDbContext<ApplicationDbContext>(options =>
{
    // Use InMemory database for development
    // TODO: Replace with SQL Server for production
    options.UseInMemoryDatabase("PapaganCMS");
});

// Add ASP.NET Identity
builder.Services.AddIdentity<ApplicationUser, IdentityRole>(options =>
{
    // Password settings
    options.Password.RequireDigit = true;
    options.Password.RequireLowercase = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireNonAlphanumeric = false;
    options.Password.RequiredLength = 8;

    // User settings
    options.User.RequireUniqueEmail = true;

    // Sign in settings
    options.SignIn.RequireConfirmedEmail = false;
})
.AddEntityFrameworkStores<ApplicationDbContext>()
.AddDefaultTokenProviders();

// Configure cookie authentication
builder.Services.ConfigureApplicationCookie(options =>
{
    options.Cookie.HttpOnly = true;
    options.ExpireTimeSpan = TimeSpan.FromDays(7);
    options.LoginPath = "/login";
    options.LogoutPath = "/logout";
    options.AccessDeniedPath = "/access-denied";
    options.SlidingExpiration = true;
});

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();

// Add API controllers
builder.Services.AddControllers()
    .AddNewtonsoftJson(); // Required for Stripe webhook processing

// Add HttpContextAccessor
builder.Services.AddHttpContextAccessor();

// Configure HttpClient for chat agent backend
var backendUrl = builder.Configuration["ChatAgent:BackendUrl"] ?? "http://localhost:5000";
builder.Services.AddHttpClient("ChatBackend", client =>
{
    client.BaseAddress = new Uri(backendUrl);
    client.Timeout = TimeSpan.FromSeconds(30);
});

// Register application services
builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IBotService, BotService>();
builder.Services.AddScoped<IOnboardingService, OnboardingService>();

// Register subscription services (using OrkinosaiCMS namespace)
builder.Services.AddSingleton<OrkinosaiCMS.Core.Interfaces.Services.IUserService, UserService>();
builder.Services.AddSingleton<ICustomerService, CustomerService>();
builder.Services.AddSingleton<ISubscriptionService, SubscriptionService>();
builder.Services.AddScoped<IStripeService, StripeService>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseWebAssemblyDebugging();
}
else
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}
app.UseStatusCodePagesWithReExecute("/not-found", createScopeForStatusCodePages: true);
app.UseHttpsRedirection();

// Add authentication and authorization
app.UseAuthentication();
app.UseAuthorization();

app.UseAntiforgery();

app.MapStaticAssets();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode()
    .AddAdditionalAssemblies(typeof(PapaganCMS.Client._Imports).Assembly);

// Map API controllers
app.MapControllers();

app.Run();
