using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PapaganCMS.Infrastructure.Data.Migrations
{
    /// <inheritdoc />
    public partial class AddBotModelRouting : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "FallbackModel",
                table: "Bots",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: false,
                defaultValue: "sumotx");

            migrationBuilder.AddColumn<string>(
                name: "PrimaryModel",
                table: "Bots",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: false,
                defaultValue: "gpt-4");

            migrationBuilder.AddColumn<string>(
                name: "RoutingMode",
                table: "Bots",
                type: "nvarchar(50)",
                maxLength: 50,
                nullable: false,
                defaultValue: "auto");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "FallbackModel",
                table: "Bots");

            migrationBuilder.DropColumn(
                name: "PrimaryModel",
                table: "Bots");

            migrationBuilder.DropColumn(
                name: "RoutingMode",
                table: "Bots");
        }
    }
}
