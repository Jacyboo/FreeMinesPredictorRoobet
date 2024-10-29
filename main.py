import discord
from discord.ext import commands
import random
#This is free code for a random predictor discord bot. You can sell it for money
#Code by jacxdisx on discord dm me for help
TOKEN = "" #Change to ur token

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

UNKNOWN_EMOJI = "❔"
BOMB_EMOJI = "💣"
GEM_EMOJI = "💎"


def mines_prediction(seed: str, mine_count: int):
    random.seed(seed)
    grid_size = 5
    total_cells = grid_size * grid_size

    # Limit mines to prevent overcrowding
    mine_count = max(1, min(mine_count, total_cells - 5))

    # Generate unique mine positions
    mines = set()
    while len(mines) < mine_count:
        mines.add(random.randint(0, total_cells - 1))

    # Build the grid with bombs and unknowns, add a few gems for variety
    grid = [BOMB_EMOJI if i in mines else UNKNOWN_EMOJI for i in range(total_cells)]
    gem_positions = random.sample([i for i in range(total_cells) if i not in mines], k=min(3, total_cells - mine_count))
    for pos in gem_positions:
        grid[pos] = GEM_EMOJI

    # Format grid into rows
    grid_display = ""
    for row in range(grid_size):
        grid_display += " ".join(grid[row * grid_size:(row + 1) * grid_size]) + "\n"

    return grid_display, mines


@bot.event
async def on_ready():
    print(f"{bot.user} is online.")


@bot.command(name="predict_mines")
async def predict_mines(ctx, client_seed: str, mine_count: int):
    if not (1 <= mine_count <= 25):
        await ctx.send("Enter a valid number of mines (1-25).")
        return

    grid_display, mines = mines_prediction(client_seed, mine_count)

    embed = discord.Embed(
        title="FREE UNBRANDED PREDICTOR", #Change Name to ur predictor name
        description="Roobet Mines Prediction Tool", # Change to whatever
        color=discord.Color.blue()
    )
    embed.add_field(name="Client Seed", value=f"`{client_seed}`", inline=False)
    embed.add_field(name="Number of Mines", value=f"{mine_count}", inline=False)
    embed.add_field(name="Predicted Mine Grid", value=grid_display, inline=False)
    embed.set_footer(text="FREE UNBRANDED PREDICTOR") #Change to ur name
    embed.set_thumbnail(url="https://example.com/your_logo.png")  # Change to your logo

    await ctx.send(embed=embed)


bot.run(TOKEN)
