using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Identity.Web;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

using api.Data;
using api.Environment;

// Function to check if all properties are defined/set
bool AreAllPropertiesNotNull(object obj, params string[] excludedProperties)
{
    if (obj == null) return false;

    return obj.GetType().GetProperties()
        .Where(p => !excludedProperties.Contains(p.Name))
        .All(p => p.GetValue(obj) != null);
}

//// Make sure environment variables defined
//if (AreAllPropertiesNotNull(Variables) {
//    throw new Exception("Environemnt Variables don't all contain a definition");
//}

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<DataContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DataContext") ?? throw new InvalidOperationException("Connection string 'DataContext' not found.")));

// Add services to the container.
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));

builder.Services.AddControllers();

var app = builder.Build();

// Configure the HTTP request pipeline.

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
