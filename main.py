from config import TOKEN
# Kodun yarısı Chat GPT tarafından oluşturuldu (sanayi dalı örneği)

import discord
from discord.ext import commands
from discord.ui import View, Button

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# --- KARIYER AĞACI (BRANCHING) ---

CAREER_TREE = {
    "start": {
        "text": "Hangi meslek alanı ile ilgileniyorsun?",
        "options": {
            "Sanayi": "sanayi_1",
            "Yazılım": "yazilim_1",
            "Sağlık": "saglik_1"
            ""
        }
    },

    # --- SANAYİ DALINDAKİ SORULAR ---
    "sanayi_1": {
        "text": "Sanayide hangi dal sana daha yakın?",
        "options": {
            "Otomotiv": "sanayi_otomotiv",
            "Makine sanayi": "sanayi_makine",
            "Gıda sanayi": "sanayi_gida",
            "Kimya": "sanayi_kimya",
        }
    },

    "sanayi_otomotiv": {
        "text": "Otomotiv sanayisi... İlginç! Hangi alanda çalışmak istersin?",
        "options": {
            "Tamir & bakım": "final_tamir",
            "Üretim hattı": "final_uretim",
            "Tasarım (CAD)": "final_tasarim"
        }
    },

    "sanayi_makine": {
        "text": "Makine sanayisi seçildi! Neye ilgin var?",
        "options": {
            "CNC Operatörlüğü": "final_cnc",
            "Montaj teknisyenliği": "final_montaj"
        }
    },

    "sanayi_gida": {
        "text": "Gıda sanayisi! Hangi alanı tercih edersin?",
        "options": {
            "İçecekler": "final_icecek",
            "Pastacılık": "final_pasta"
        }
    },

    # --- YAZILIM DALINDAKİ SORULAR ---
    "yazilim_1": {
        "text": "Yazılımda hangi dal sana daha yakın?",
        "options": {
            "Web Geliştirme": "yz_web",
            "Mobil uygulama Geliştirme": "yz_mobil",
            "Oyun Geliştirme": "yz_oyun"
        }
    },
    # --- SAĞLIK DALINDAKİ SORULAR ---
    "saglik_1": {
        "text": "Sağlıkta hangi dal sana daha yakın?",
        "options": {
            "Doktorluk": "sg_doktor",
            "Laboratuvarlar": "sg_lab",
            "Eczacılık": "sg_eczaci"
        }
    },

    "sg_doktor": {
        "text": "Doktorluk alanında hangi branş ilgini çekiyor?",
        "options": {
            "Çocuk Hastalıkları": "final_genel_cerrahi",
            "Göz Hastalıkları": "final_dahiliye",
            "Göğüs": "final_pediatri"
        }
    },






















































    # --- FİNAL CEVAPLAR ---
    "final_tamir": {
        "text": "Tamir & bakım alanı sana uygun olabilir!"
    },
    "final_uretim": {
        "text": "Üretim hattında çalışmak sana göre!"
    },
    "final_tasarim": {
        "text": "CAD tasarım alanı tam sana göre olabilir!"
    },
    "final_cnc": {
        "text": "CNC operatörlüğü geleceği parlak bir seçim!"
    },
    "final_montaj": {
        "text": "Montaj teknisyenliği güzel bir alan!"
    },
    "final_devre": {
        "text": "Elektronik devre tasarımı tam sana göre!"
    },
    "final_elektronik_tamir": {
        "text": "Elektronik tamir alanında başarılı olabilirsin!"
    },
    "yazilim_1": {
        "text": "Yazılım alanı yakında eklenecek!",
        "options": {}
    },
    "saglik_1": {
        "text": "Sağlık alanı yakında eklenecek!",
        "options": {}
    }
}


# ---- VIEW VE BUTONLAR ----

class CareerView(View):
    def __init__(self, ctx, node_id):
        super().__init__(timeout=20)
        self.ctx = ctx
        self.node_id = node_id
        data = CAREER_TREE[node_id]

        # Butonları ekle
        for label, next_node in data.get("options", {}).items():
            self.add_item(CareerButton(label, next_node, ctx))


class CareerButton(Button):
    def __init__(self, label, next_node, ctx):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)
        self.next_node = next_node
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(
                "Bu kariyer yönlendirmesi sana ait!", ephemeral=True
            )

        node = CAREER_TREE[self.next_node]


        view = CareerView(self.ctx, self.next_node) if node.get("options") else None

        await interaction.response.edit_message(
            content=f"**{node['text']}**",
            view=view
        )
@bot.command()
async def kariyer(ctx):
    start = CAREER_TREE["start"]
    view = CareerView(ctx, "start")

    await ctx.send(f"**{start['text']}**", view=view)


@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")



bot.run(TOKEN)
