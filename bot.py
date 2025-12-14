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
            "Web Geliştirme": "final_web",
            "Mobil uygulama Geliştirme": "final_mobil",
            "Oyun Geliştirme": "final_oyun"
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
            "Çocuk Hastalıkları": "final_cocukh",
            "Göz Hastalıkları": "final_goz",
            "Göğüs": "final_gogus"
        }
    },
    
    "sg_lab": {
        "text": "Laboratuvar alanında hangi branş ilgini çekiyor? (Seçeneklerinizi araştırınız!)",
        "options": {
            "Hematoloji": "final_hemato",
            "Mikrobiyoloji": "final_mikro",
            "Referans laboratuvarı": "final_reflab"
        }
    },

    "sg_eczaci": {
        "text": "Eczacılık alanında hangi branş ilgini çekiyor? (Seçeneklerinizi araştırınız!)",
        "options": {
            "Klinik eczacılık": "final_klinik",
            "Endüstri eczacılığı": "final_endustri",
            "Adli eczacılık": "final_adli"
        }
    },

    # --- FİNAL CEVAPLAR ---
    "final_tamir": {
        "text": "Otomotiv tamir ve bakım teknisyeni olabilirsin!"
    },
    "final_uretim": {
        "text": "Otomotiv üretim hattında çalışabilirsin!"
    },
    "final_tasarim": {
        "text": "Otomotiv tasarımcısı (CAD) olabilirsin!"
    },
    "final_web": {
        "text": "Web geliştiricisi olabilirsin!"
    },
    "final_mobil": {
        "text": "Mobil uygulama geliştiricisi olabilirsin!"
    },
    "final_oyun": {
        "text": "Oyun geliştiricisi olabilirsin!"
    },
    "final_cocukh": {
        "text": "Çocuk hastalıkları doktoru olabilirsin!"
    },
    "final_goz": {
        "text": "Göz hastalıkları doktoru olabilirsin!"
    },
    "final_gogus": {
        "text": "Göğüs hastalıkları doktoru olabilirsin!"
    },
    "final_hemato": {
        "text": "Hematoloji laboratuvarında çalışabilirsin!"
    },
    "final_mikro": {
        "text": "Mikrobiyoloji laboratuvarında çalışabilirsin!"
    },
    "final_reflab": {
        "text": "Referans laboratuvarında çalışabilirsin!"
    },
    "final_klinik": {
        "text": "Klinik eczacısı olabilirsin!"
    },
    "final_endustri": {
        "text": "Endüstri eczacısı olabilirsin!"
    },
    "final_adli": {
        "text": "Adli eczacısı olabilirsin!"
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
                "Bu kariyer sana daha çok uyuyor!", ephemeral=True
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
