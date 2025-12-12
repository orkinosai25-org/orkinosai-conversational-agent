using PapaganCMS.Client.Pages;
using PapaganCMS.Components;
using PapaganCMS.Core.Interfaces.Services;
using PapaganCMS.Infrastructure.Services;
using PapaganCMS.Infrastructure.Services.Subscriptions;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();

// Add API controllers
builder.Services.AddControllers()
    .AddNewtonsoftJson(); // Required for Stripe webhook processing

// Configure HttpClient for chat agent backend
var backendUrl = builder.Configuration["ChatAgent:BackendUrl"] ?? "http://localhost:5000";
builder.Services.AddHttpClient("ChatBackend", client =>
{
    client.BaseAddress = new Uri(backendUrl);
    client.Timeout = TimeSpan.FromSeconds(30);
});

// Register subscription services
builder.Services.AddSingleton<IUserService, UserService>();
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

app.UseAntiforgery();

app.MapStaticAssets();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode()
    .AddAdditionalAssemblies(typeof(OrkinosaiCMS.Client._Imports).Assembly);

// Map API controllers
app.MapControllers();

app.Run();
