using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace SiteChatCMS.Infrastructure.Data;

/// <summary>
/// Design-time factory used by <c>dotnet ef migrations</c> tooling.
/// It provides a SQL Server context so that migrations can be scaffolded
/// without running the full application (which defaults to InMemory in dev).
/// <para>
/// The connection string is resolved at design time from the
/// <c>CONNECTIONSTRINGS__DEFAULT</c> environment variable (or from
/// <c>dotnet user-secrets</c>).  Set it before running migration commands:
/// <code>
///   export CONNECTIONSTRINGS__DEFAULT="Server=tcp:localhost,1433;..."
///   dotnet ef migrations add &lt;Name&gt;
/// </code>
/// </para>
/// </summary>
public class ApplicationDbContextDesignTimeFactory : IDesignTimeDbContextFactory<ApplicationDbContext>
{
    public ApplicationDbContext CreateDbContext(string[] args)
    {
        var connectionString = Environment.GetEnvironmentVariable("CONNECTIONSTRINGS__DEFAULT")
            ?? throw new InvalidOperationException(
                "Set the CONNECTIONSTRINGS__DEFAULT environment variable to a valid SQL Server " +
                "connection string before running 'dotnet ef' commands.");

        var optionsBuilder = new DbContextOptionsBuilder<ApplicationDbContext>();
        optionsBuilder.UseSqlServer(connectionString);

        return new ApplicationDbContext(optionsBuilder.Options);
    }
}
